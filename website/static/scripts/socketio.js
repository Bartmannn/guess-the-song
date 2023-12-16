var startButton = document.getElementById("start_game_button");
var nextButton = document.getElementById("next_round_button");
var songsChoice = document.getElementById("songs");
var mediaPlayer = document.getElementById("audioPlayer");
console.log(mediaPlayer)
var cathegory = "";

document.addEventListener("DOMContentLoaded", () => {
    var socket = io();

    if (is_admin) {
        startButton.disabled = false;
    } else if (!is_admin) {
        startButton.disabled = true;
    }
    
    current_round = 0;
    joinRoom(room_name);
    var audioPlayer = document.getElementById("audioPlayer");
    socket.emit("list_players", code);
    printSysMsg("To start click \"Next round\" button.");

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
        current_round += 1;
        if (current_round % 10 == 0) {
            startButton.style.display = "block";
            nextButton.style.display = "none";

            songsChoices.style.display = "block";
            audioPlayer.style.display = "none";
            return;
        }
        // document.querySelector("#current_round").innerHTML = current_round + ". round";
        printSysMsg(current_round + ". round");

        var audioSource = document.getElementById('audioSource');

        var blob = new Blob([data.audio_data], { type: 'audio/mpeg' });
        var url = URL.createObjectURL(blob);

        audioPlayer.currentTime += 15;
        audioSource.src = url;
        audioPlayer.load();
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

    // Send message
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector("#user_message").value, "username": username, "room": room_name});
        document.querySelector("#user_message").value = "";
    }

    document.querySelector("#next_round_button").onclick = () => {
        socket.emit("request_audio", {"room": room_name, "round": current_round, "cathegory": cathegory});
    }

    startButton.onclick = () => {
        startButton.style.display = "none";
        nextButton.style.display = "block";

        songsChoice.style.display = "none";
        mediaPlayer.style.display = "block";

        cathegory = songsChoice.value

        socket.emit('request_audio', {"room": room_name, "round": current_round, "cathegory": cathegory});
    }

    // Leave room
    function leaveRoom(room) {
        // socket.emit("leave", {"username": username, "room": room});
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

    window.onbeforeunload = function() {
        leaveRoom(code);
    }

});