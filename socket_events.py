from flask import request
from flask_socketio import emit

clients = {}
admin_connections = set()
chat_history = {}

def register_socket_events(socketio):
    # funcion para ver si el estatius del admin
    def emit_admin_status():
        status = len(admin_connections) > 0
        for sid in clients:
            socketio.emit("admin_status", {"connected": status}, room=sid)

    @socketio.on("connect")
    def on_connect():
        print(f"Conectado: {request.sid}")

    @socketio.on("set_role")
    def handle_set_role(role):
        if role == "admin":
            admin_connections.add(request.sid)
            emit("client_list", [{"sid": sid, "username": data["username"]} for sid, data in clients.items()], room=request.sid)
            emit_admin_status()
        else:
            username = f"Cliente {len(clients)+1}"
            clients[request.sid] = {"username": username}
            for admin_sid in admin_connections:
                emit("client_list", [{"sid": sid, "username": data["username"]} for sid, data in clients.items()], room=admin_sid)
            emit_admin_status()

    @socketio.on("client_to_admin")
    def handle_client_message(data):
        sid = request.sid
        message = data["message"]
        chat_history.setdefault(sid, []).append({"from": "client", "message": message})
        for admin_sid in admin_connections:
            emit("admin_receive", {"sid": sid, "message": message}, room=admin_sid)

    @socketio.on("admin_to_client")
    def handle_admin_message(data):
        sid = data["sid"]
        message = data["message"]
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
        was_admin = request.sid in admin_connections
        admin_connections.discard(request.sid)
        for admin_sid in admin_connections:
            emit("client_list", [{"sid": sid, "username": data["username"]} for sid, data in clients.items()], room=admin_sid)
        if was_admin:
            emit_admin_status()
