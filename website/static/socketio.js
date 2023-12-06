var socket = io();

document.addEventListener("DOMContentLoaded", () => {
    
    joinRoom(room_name);
    socket.emit('request_audio');

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

    socket.on('stream_audio', function(data) {
        var audioPlayer = document.getElementById('audioPlayer');
        var audioSource = document.getElementById('audioSource');

        var blob = new Blob([data.audio_data], { type: 'audio/mpeg' });
        var url = URL.createObjectURL(blob);

        audioSource.src = url;
        audioPlayer.load();
    });

    socket.on("list_players", data => {
        if (code == data["code"]) {
            document.querySelector("#users_list").innerHTML = "";
            var players_list = data["players"];
            var li;
            for (var i = 0; i < players_list.length; i++) {
                li = document.createElement("li");
                li.innerHTML = players_list[i];
                document.querySelector("#users_list").append(li);
            }
        }
    });

    // Send message
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector("#user_message").value, "username": username, "room": room_name});
        document.querySelector("#user_message").value = "";
    }

    // Leave room
    function leaveRoom(room) {
        socket.emit("leave", {"username": username, "room": room});
    }

    // Join room
    function joinRoom(room) {
        socket.emit("join", {"username": username, "room": room});
        socket.emit("list_players", code);
    }

    function printSysMsg(msg) {
        const p = document.createElement("p");
        p.innerHTML = msg;
        p.style = "font-size: 1rem;";
        document.querySelector("#messages_area").append(p);
    }

    window.onbeforeunload = function() {
        leaveRoom(code);
    }

});