const socket = io();

socket.on('connect', () => {
    console.log('Conectado al servidor');
});

socket.on('message', function(msg) {
    const item = document.createElement('li');
    item.textContent = msg;
    document.getElementById('messages').appendChild(item);
});

function sendMessage() {
    const input = document.getElementById('myMessage');
    const msg = input.value;
    socket.send(msg);
    input.value = '';
}
