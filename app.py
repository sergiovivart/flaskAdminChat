from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.secret_key = 'esto_es_mi_clave_super_secreta_123'
socketio = SocketIO(app)

clients = {}
admin_connections = set()
chat_history = {}  # Clave: sid del cliente, valor: lista de mensajes


#  las vistas normales
@app.route("/")
def client():
    return render_template("client.html")

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    return render_template("admin.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == 'admin' and request.form["password"] == 'admin':
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("login"))



# los eventos del socketio se ejecutan en el servidor
@socketio.on("connect")
def on_connect():
    print(f"Conectado: {request.sid}")

# orgnaizamos los roles
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

# envia el mensaje al admin
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

#envia el mensaje al cliente
@socketio.on("admin_to_client")
def handle_admin_message(data):
    sid = data["sid"]
    message = data["message"]
    print(f"Admin responde a {sid}: {message}")

    # Guardar historial
    chat_history.setdefault(sid, []).append({"from": "admin", "message": message})

    emit("client_receive", {"message": message}, room=sid)

#pide el historial de mensajes
@socketio.on("request_chat_history")
def handle_chat_history_request(data):
    sid = data["sid"]
    history = chat_history.get(sid, [])
    emit("chat_history", {"sid": sid, "history": history}, room=request.sid)

# en desconexión se elimina el cliente de la lista
@socketio.on("disconnect")
def on_disconnect():
    print(f"Desconectado: {request.sid}")
    clients.pop(request.sid, None)
    admin_connections.discard(request.sid)
    for admin_sid in admin_connections:
        emit("client_list", [{"sid": sid, "username": data["username"]} for sid, data in clients.items()], room=admin_sid)

if __name__ == "__main__":
    socketio.run(app, debug=True)
