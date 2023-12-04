document.addEventListener("DOMContentLoaded", () => {
    var socket = io();

    joinRoom(room_name);

    // Display messages
    socket.on("message", data => {
        const p = document.createElement("p");
        const span_username = document.createElement("span");

        span_username.style = "font-size: 1rem; color: darkgrey;";

        const br = document.createElement("br");

        if (data.username) {
            span_username.innerHTML = data.username;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg;
            document.querySelector("#messages_area").append(p);
        } else {
            printSysMsg(data.msg);
        }
    });

    // Send message
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector("#user_message").value, "username": username, "room": room_name});
        // Clear input area
        document.querySelector("#user_message").value = "";
    }

    // Leave room
    function leaveRoom(room) {
        socket.emit("leave", {"username": username, "room": room});
    }

    // Join room
    function joinRoom(room) {
        socket.emit("join", {"username": username, "room": room})

        const li = document.createElement("li");
        li.innerHTML = username;


        document.querySelector("#users_list").append(li);

        document.querySelector("#messages_area").innerHTML = "";
        document.querySelector("#user_message").focus();
    }

    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement("p");
        p.innerHTML = msg;
        p.style = "font-size: 1rem;";
        document.querySelector("#messages_area").append(p);
    }

});