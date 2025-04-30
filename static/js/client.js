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
    makeListItem(msg.message , 'from-client');
});

socket.on("admin_status", (data) => {
    const statusElem = document.getElementById("admin-status");
    if (data.connected) {
        statusElem.innerText = "Administrador disponible";
        // statusElem.className = "text-success fw-bold";
    } else {
        statusElem.innerText = "No disponible";
        // statusElem.className = "text-danger fw-bold";
    }
});

// LAS FUNCIONES

function sendClientMessage() {
    const msg = document.getElementById("clientMessage").value;
    if (msg === '') {
        alert("Please enter a message.");
        return;
    }
    socket.emit("client_to_admin", { message: msg });
    document.getElementById("clientMessage").value = '';
    makeListItem(msg , 'from-admin');
}

function showChat() {
    document.getElementById('containerChat').style.display = 'block';
}

function closeChat() {
    document.getElementById('containerChat').style.display = 'none';
}
