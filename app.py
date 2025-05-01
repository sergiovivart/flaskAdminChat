from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
from socket_events import register_socket_events
from routes.main_routes import main  # importa el blueprint
# from sockets import register_socketio_events # eventos de socketio


app = Flask(__name__)
app.secret_key = 'esto_es_mi_clave_super_secreta_123'
socketio = SocketIO(app)

clients = {}
admin_connections = set()
chat_history = {}  # Clave: sid del cliente, valor: lista de mensajes

# registramos rutas
app.register_blueprint(main)  

# eventos de socketio
register_socket_events(socketio)

if __name__ == "__main__":
    socketio.run(app, debug=True)
