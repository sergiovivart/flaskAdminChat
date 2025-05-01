
from app import app, socketio

def test_client_connection_and_role():
    test_client = socketio.test_client(app)
    assert test_client.is_connected()

    # Simula que el cliente se identifica como cliente
    test_client.emit('set_role', 'client')
    received = test_client.get_received()

    # Deberías ver que no hay errores y se actualiza la lista del admin (aunque no se devuelva nada al cliente)
    print("Received after setting role:", received)

    test_client.disconnect()
    assert not test_client.is_connected()

def test_admin_connection_and_receive_clients():
    admin_client = socketio.test_client(app)
    assert admin_client.is_connected()

    # El admin se identifica como tal
    admin_client.emit('set_role', 'admin')
    received = admin_client.get_received()

    # El admin debería recibir una lista de clientes (probablemente vacía)
    assert any(r['name'] == 'client_list' for r in received)

    print("Admin received client list:", received)

    admin_client.disconnect()