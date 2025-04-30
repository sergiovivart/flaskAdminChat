const socket = io();
socket.emit("set_role", "client");

// para hacer los item de la lista
function makeListItem(msg , nombreClases) {
    const li = document.createElement("li");
    li.textContent = msg;
    li.classList.add('message-bubble');
    li.classList.add(nombreClases);
    document.getElementById("chatLog").appendChild(li);
}   

socket.on('client_receive', msg => {
    makeListItem(`Admin: ${msg.message}` , 'from-client');
});

function sendClientMessage() {
    const msg = document.getElementById("clientMessage").value;
    socket.emit("client_to_admin", { message: msg });
    document.getElementById("clientMessage").value = '';
    makeListItem(`Tu: ${msg}` , 'from-admin');
}
