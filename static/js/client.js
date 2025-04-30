const socket = io();
socket.emit("set_role", "client");

// para hacer los item de la lista
function makeListItem(msg , nombreClases) {
    const li = document.createElement("li");
    li.textContent = msg;
    li.classList.add(nombreClases);
    document.getElementById("chatLog").appendChild(li);
}   

socket.on('client_receive', msg => {
    makeListItem(`[ADMIN]: ${msg}` , 'recivido');
});

function sendClientMessage() {
    const msg = document.getElementById("clientMessage").value;
    socket.emit("client_to_admin", { message: msg });
    document.getElementById("clientMessage").value = '';
    makeListItem(`[YO]: ${msg}` , 'enviado');
}
