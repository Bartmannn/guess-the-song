document.addEventListener("DOMContentLoaded", () => {
    var socket = io();

    // let room = "Longue";
    // joinRoom("Longue");

    // Display messages
    socket.on("message", data => {
        const p = document.createElement("p");
        const span_username = document.createElement("span");
        // const span_timestamp = document.createElement("span");
        const br = document.createElement("br");

        p.innerHTML = data.msg
        document.querySelector("#messages_area").append(p);

        if (data.username) {
            span_username.innerHTML = data.username;
            p.innerHTML = span_username + br + data.msg
            document.querySelector("#messages_area").append(p);
        } else {
            printSysMsg(data.msg);
        }
    });

    // Send message
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector("#user_message").value});
        // Clear input area
        document.querySelector("#user_message").value = "";
    }

    // Room selection
    // document.querySelectorAll(".select-room").forEach(p => {
    //     p.onclick = () => {
    //         let newRoom = p.innerHTML;
    //         if (newRoom == room) {
    //             msg = `You are already in ${room} room.`
    //             printSysMsg(msg);
    //         } else {
    //             leaveRoom(room);
    //             joinRoom(newRoom);
    //             room = newRoom;
    //         }
    //     }
    // });

    // Leave room
    function leaveRoom(room) {
        socket.emit("leave", {"username": username, "room": room});
    }

    // Join room
    function joinRoom(room) {
        socket.emit("join", {"username": username, "room": room})
        // Clear message area
        document.querySelector("#messages-section").innerHTML = "";
        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }

    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement("p");
        p.innerHTML = msg;
        document.querySelector("#messages-section").append(p);
    }

});