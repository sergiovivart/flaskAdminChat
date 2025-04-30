const socket = io();
socket.emit("set_role", "client");

socket.on('client_receive', msg => {
    const li = document.createElement("li");
    li.textContent = `[ADMIN]: ${msg}`;
    document.getElementById("chatLog").appendChild(li);
});

function sendClientMessage() {
    const msg = document.getElementById("clientMessage").value;
    socket.emit("client_to_admin", { message: msg });
    document.getElementById("clientMessage").value = '';
}
