var startButton = document.getElementById("start_game_button");
var nextButton = document.getElementById("next_round_button");
var songsChoice = document.getElementById("songs");
var mediaPlayer = document.getElementById("audioPlayer");
var audioSource = document.getElementById('audioSource');
var cathegory = "";

document.addEventListener("DOMContentLoaded", () => {
    var socket = io();
    var isPreparing = false;

    joinRoom();
    // updateState()

    var audioPlayer = document.getElementById("audioPlayer");
    socket.emit("list_players", room_name);
    printSysMsg("To start click \"Start\" button.");
    printSysMsg("To guess song type \"\\<your guess>\" and send.")

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
        isPreparing = false;
        nextButton.disabled = false;

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
        printSysMsg(data.msg);
    });

    socket.on("start_game", () => {
        isPreparing = false;
        startButton.disabled = false;
        nextButton.disabled = false;
        startButton.style.display = "none";
        nextButton.style.display = "block";

        songsChoice.style.display = "none";
        mediaPlayer.style.display = "block";
    });

    socket.on("preparing_game", data => {
        isPreparing = true;
        startButton.disabled = true;
        nextButton.disabled = true;
    });

    socket.on("prepare_failed", data => {
        isPreparing = false;
        startButton.disabled = false;
        nextButton.disabled = false;
    });

    socket.on("game_over", () => {
        isPreparing = false;
        startButton.disabled = false;
        nextButton.disabled = false;
        if (audioSource.src[0] != "h") {
            audioPlayer.currentTime += 15;
        }

        startButton.style.display = "block";
        nextButton.style.display = "none";

        songsChoice.style.display = "block";
        mediaPlayer.style.display = "none";
    });

    socket.on("update_state", () => {
        startButton.style.display = "none";
        nextButton.style.display = "block";
        nextButton.disabled = false;
        songsChoice.style.display = "none";
        mediaPlayer.style.display = "block";

        // socket.emit("update_state")
    });

    // Send message
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector("#user_message").value, "username": username, "room": room_name, "is_admin": is_admin});
        document.querySelector("#user_message").value = "";
    }

    document.querySelector("#next_round_button").onclick = () => {
        if (isPreparing) {
            return;
        }
        socket.emit("request_audio", {"room": room_name});
    }

    startButton.onclick = () => {
        if (isPreparing) {
            return;
        }
        cathegory = songsChoice.value
        socket.emit('start', {"room": room_name, "cathegory": cathegory});
    }

    // Leave room
    function leaveRoom() {
        socket.emit("leave", {"username": username, "room": room});
    }

    // Join room
    function joinRoom() {
        socket.emit("join", {"username": username, "room": room_name});
        socket.emit("update_state", {"room": room_name});
    }

    // function getCurrentState() {
    //     socket.emit("update_state", {"username"})
    // }

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
