const socket = io();
socket.emit("set_role", "admin");

let selectedClient = null;

// Mostrar el socket ID del cliente seleccionado
socket.on('connect', () => {
    document.getElementById("adminSocketId").textContent = socket.id;
});

socket.on('admin_receive', data => {
    const li = document.createElement("li");
    li.textContent = `[${data.sid}]: ${data.message}`;
    document.getElementById("chatLog").appendChild(li);
});

socket.on('client_list', clients => {
    const list = document.getElementById("clientList");
    list.innerHTML = '';
    clients.forEach(client => {
        const li = document.createElement("li");
        li.textContent = client.username;
        li.onclick = () => selectClient(client);
        list.appendChild(li);
    });
});

function selectClient(client) {
    selectedClient = client.sid;
    document.getElementById("selectedClientSocketId").textContent = selectedClient;
}

function sendAdminMessage() {
    const msg = document.getElementById("adminMessage").value;
    if (selectedClient) {
        socket.emit("admin_to_client", { sid: selectedClient, message: msg });
        document.getElementById("adminMessage").value = '';

        // hacemos el componente
        const li = document.createElement("li");
        li.textContent = `[FROM ADMIN TO : ${selectedClient} ]: ${msg}`;
        document.getElementById("chatLog").appendChild(li);
    } else {
        alert("Selecciona un cliente.");
    }
}
