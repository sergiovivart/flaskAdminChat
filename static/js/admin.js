const socket = io();
socket.emit("set_role", "admin");

let selectedClient = null;

// Mostrar el socket ID del cliente seleccionado
socket.on('connect', () => {
    document.getElementById("adminSocketId").textContent = socket.id;
});


// los eventos de los mensajes
socket.on("admin_receive", data => {
    const { sid, message } = data;

    if (selectedClient === sid) {
        const li = document.createElement("li");
        li.classList.add("message-bubble", "from-client");
        li.textContent = message;
        document.getElementById("chatLog").appendChild(li);
    } else {
        // Solo mostrar badge si el cliente NO está seleccionado
        const clientItem = document.getElementById(`client-${sid}`);
        if (clientItem && !clientItem.querySelector(".badge")) {
            const badge = document.createElement("span");
            badge.className = "badge bg-danger ms-2";
            badge.textContent = "Nuevo mensaje";
            clientItem.appendChild(badge);
        }
    }
});

socket.on("client_list", (clients) => {
    const list = document.getElementById("clientList");
    list.innerHTML = "";

    clients.forEach(client => {
        const li = document.createElement("li");
        li.id = `client-${client.sid}`;
        li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center", "cursor-pointer");
        // li.textContent = client.username;
        li.textContent = client.sid;

        li.onclick = () => {
            selectClient(client);

            // Eliminar la etiqueta de nuevo mensaje si la tenía
            const badge = li.querySelector(".badge");
            if (badge) {
                badge.remove();
            }
        };
        list.appendChild(li);
    });
});

// ver el historial del cht
socket.on("chat_history", data => {
    const log = document.getElementById("chatLog");
    log.innerHTML = "";

    data.history.forEach(entry => {
        const li = document.createElement("li");
        li.textContent = entry.message;
        li.classList.add("message-bubble");
        if (entry.from === "admin") {
            li.classList.add("from-admin");
        } else {
            li.classList.add("from-client");
        }
        log.appendChild(li);
    });

    // Scroll al final automáticamente
    log.scrollTop = log.scrollHeight;
});



// las funciones para el chat
function selectClient(client) {
    selectedClient = client.sid;
    document.getElementById("selectedClientSocketId").textContent = selectedClient;

    // Eliminar etiqueta de nuevo mensaje si existe
    const li = document.getElementById(`client-${selectedClient}`);
    const badge = li.querySelector(".badge");
    if (badge) badge.remove();

    // Limpiar chat anterior
    document.getElementById("chatLog").innerHTML = "";

    // Solicitar historial del nuevo cliente
    socket.emit("request_chat_history", { sid: selectedClient });
}

function sendAdminMessage() {
    const msg = document.getElementById("adminMessage").value;
    if (selectedClient && msg !== "") {
        socket.emit("admin_to_client", { sid: selectedClient, message: msg });
        document.getElementById("adminMessage").value = '';
        // hacemos el componente
        const li = document.createElement("li");
        li.textContent = msg;
        li.classList.add("message-bubble", "from-admin");
        document.getElementById("chatLog").appendChild(li);
    } else {
        alert("Selecciona un cliente y escribe un mensaje.");
    }
}

// para los chat guardados y demas 
function selectClient(client) {
    selectedClient = client.sid;
    document.getElementById("selectedClientSocketId").textContent = selectedClient;
    // Limpiar historial actual
    document.getElementById("chatLog").innerHTML = "";
    // Solicitar historial al backend
    socket.emit("request_chat_history", { sid: selectedClient });
}


