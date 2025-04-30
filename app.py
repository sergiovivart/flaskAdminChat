from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = {}  # { sid: { "username": ..., "role": ..., "room": ... } }

# Rutas HTML
@app.route('/client')
def client_view():
    return render_template('client.html')

@app.route('/admin')
def admin_view():
    return render_template('admin.html')

# Cuando un cliente/admin se conecta
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    clients[sid] = {
        "username": f"user_{sid[:5]}",
        "role": "client",  # por defecto
        "room": sid
    }
    print(f"Conectado: {sid}")

# Establecer el rol (lo emite el frontend al iniciar)
@socketio.on('set_role')
def handle_set_role(role):
    sid = request.sid
    if sid in clients:
        clients[sid]['role'] = role
        print(f"{sid} es ahora {role}")
        emit('client_list', get_client_list(), broadcast=True)

# Devuelve lista de clientes conectados (solo clientes normales)
def get_client_list():
    return [
        {"sid": sid, "username": data["username"]}
        for sid, data in clients.items()
        if data['role'] == 'client'
    ]

# Mensaje desde cliente al admin
@socketio.on('client_to_admin')
def handle_client_to_admin(data):
    sid = request.sid
    msg = data['message']
    print(f"[Cliente {sid}] => Admin: {msg}")
    emit('admin_receive', {"sid": sid, "message": msg}, broadcast=True)

# Mensaje del admin a un cliente específico
@socketio.on('admin_to_client')
def handle_admin_to_client(data):
    target_sid = data['sid']
    msg = data['message']
    print(f"[Admin] => Cliente {target_sid}: {msg}")
    emit('client_receive', msg, room=target_sid)

# Desconexión de cualquier usuario
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in clients:
        print(f"Desconectado: {sid}")
        del clients[sid]
        emit('client_list', get_client_list(), broadcast=True)

# Iniciar servidor
if __name__ == '__main__':
    socketio.run(app, debug=True)
