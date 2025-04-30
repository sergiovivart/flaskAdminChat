from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}
admin_connections = set()
chat_history = {}  # Clave: sid del cliente, valor: lista de mensajes

@app.route("/")
def client():
    return render_template("client.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@socketio.on("connect")
def on_connect():
    print(f"Conectado: {request.sid}")

@socketio.on("set_role")
def handle_set_role(role):
    if role == "admin":
        admin_connections.add(request.sid)
        emit("client_list", [{"sid": sid, "username": data["username"]} for sid, data in clients.items()], room=request.sid)
    else:
        username = f"Cliente {len(clients)+1}"
        clients[request.sid] = {"username": username}
        for admin_sid in admin_connections:
            emit("client_list", [{"sid": sid, "username": data["username"]} for sid, data in clients.items()], room=admin_sid)

@socketio.on("client_to_admin")
def handle_client_message(data):
    sid = request.sid
    message = data["message"]
    print(f"Cliente {sid} dice: {message}")

    # Guardar historial
    chat_history.setdefault(sid, []).append({"from": "client", "message": message})

    # Reenviar al admin
    for admin_sid in admin_connections:
        emit("admin_receive", {"sid": sid, "message": message}, room=admin_sid)

@socketio.on("admin_to_client")
def handle_admin_message(data):
    sid = data["sid"]
    message = data["message"]
    print(f"Admin responde a {sid}: {message}")

    # Guardar historial
    chat_history.setdefault(sid, []).append({"from": "admin", "message": message})

    emit("client_receive", {"message": message}, room=sid)

@socketio.on("request_chat_history")
def handle_chat_history_request(data):
    sid = data["sid"]
    history = chat_history.get(sid, [])
    emit("chat_history", {"sid": sid, "history": history}, room=request.sid)

@socketio.on("disconnect")
def on_disconnect():
    print(f"Desconectado: {request.sid}")
    clients.pop(request.sid, None)
    admin_connections.discard(request.sid)
    for admin_sid in admin_connections:
        emit("client_list", [{"sid": sid, "username": data["username"]} for sid, data in clients.items()], room=admin_sid)

if __name__ == "__main__":
    socketio.run(app, debug=True)
