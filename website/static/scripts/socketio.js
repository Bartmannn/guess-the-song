var startButton = document.getElementById("start_game_button");
var nextButton = document.getElementById("next_round_button");
var songsChoice = document.getElementById("songs");
var mediaPlayer = document.getElementById("audioPlayer");
var audioSource = document.getElementById('audioSource');
var cathegory = "";

document.addEventListener("DOMContentLoaded", () => {
    var socket = io();

    if (is_admin) {
        startButton.disabled = false;
    } else if (!is_admin) {
        startButton.disabled = true;
    }

    joinRoom(room_name);
    var audioPlayer = document.getElementById("audioPlayer");
    socket.emit("list_players", code);
    printSysMsg("To start click \"Next round\" button.");

    // Display messages
    socket.on("message", data => {
        const p = document.createElement("p");
        const span_username = document.createElement("span");
        var messages = document.querySelector("#messages_area");

        span_username.style = "font-size: 1rem; color: darkgrey;";

        const br = document.createElement("br");

        if (data.username) {
            span_username.innerHTML = data.username;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg;
            messages.append(p);
        } else {
            printSysMsg(data.msg);
        }

        if (messages.scrollTop + messages.clientHeight !== messages.scrollHeight) {
            messages.scrollTop = messages.scrollHeight;
        }
    });

    socket.on('stream_audio', data => {
        if (audioSource.src[0] != "h") {
            audioPlayer.currentTime += 15;
        }

        var blob = new Blob([data.audio_data], { type: 'audio/mpeg' });
        var url = URL.createObjectURL(blob);

        audioSource.src = url;
        audioPlayer.load();
        audioPlayer.play();

        console.log("Playing");
    });

    socket.on("list_players", data => {
        document.querySelector("#users_list").innerHTML = "";
        var players_list = data["players"];
        var li;
        for (var i = 0; i < players_list.length; i++) {
            li = document.createElement("li");
            li.innerHTML = players_list[i];
            document.querySelector("#users_list").append(li);
        }
    });

    socket.on("server_info", data => {
        const p = document.createElement("p");
        const span_username = document.createElement("span");
        const br = document.createElement("br");
        var messages = document.querySelector("#messages_area");

        span_username.style = "font-size: 1rem; color: darkgrey;";

        span_username.innerHTML = "Serwer";
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg;
        messages.append(p);

        if (messages.scrollTop + messages.clientHeight !== messages.scrollHeight) {
            messages.scrollTop = messages.scrollHeight;
        }
    });

    socket.on("start_game", () => {
        startButton.style.display = "none";
        nextButton.style.display = "block";

        songsChoice.style.display = "none";
        mediaPlayer.style.display = "block";
    });

    socket.on("game_over", () => {
        startButton.style.display = "block";
        nextButton.style.display = "none";

        songsChoice.style.display = "block";
        mediaPlayer.style.display = "none";

        printSysMsg("Gra zakończona!");
    });

    // Send message
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector("#user_message").value, "username": username, "room": room_name});
        document.querySelector("#user_message").value = "";
    }

    document.querySelector("#next_round_button").onclick = () => {
        socket.emit("request_audio", {"room": room_name});
    }

    startButton.onclick = () => {
        cathegory = songsChoice.value
        socket.emit('start', {"room": room_name, "cathegory": cathegory});
    }

    // Leave room
    function leaveRoom(room) {
        socket.emit("leave", {"username": username, "room": room});
    }

    // Join room
    function joinRoom(room) {
        socket.emit("join", {"username": username, "room": room});
    }

    function printSysMsg(msg) {
        const p = document.createElement("p");
        p.innerHTML = msg;
        p.style = "font-size: 1rem;";
        document.querySelector("#messages_area").append(p);
    }

    // window.onbeforeunload = function() {
    //     leaveRoom(code);
    // }

});