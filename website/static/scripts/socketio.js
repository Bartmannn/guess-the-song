/**
 * Kod JavaScript dla zdefiniowania logiki gry oraz przechwytywania komunikatów z serwera za pomocą Socket.IO. 
 */

var startButton = document.getElementById("start_game_button");
var nextButton = document.getElementById("next_round_button");
var songsChoice = document.getElementById("songs");
var mediaPlayer = document.getElementById("audioPlayer");
var audioSource = document.getElementById('audioSource');
var cathegory = "";

/**
 * Wykonuje poniższy kod po pełnym załadowaniu DOM strony.
 * @event DOMContentLoaded
 */
document.addEventListener("DOMContentLoaded", () => {
    var socket = io();

    joinRoom();

    var audioPlayer = document.getElementById("audioPlayer");
    socket.emit("list_players", room_name);
    printSysMsg("To start click \"Next round\" button.");
    printSysMsg("To guess song type \"\\<your guess>\" and send.")

    /**
     * Przechwytywanie wiadomości użytkowników z serwera oraz ich wyświetlanie.
     * @event message
     */
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

    /**
     * Prośba z serwera o odtwarzanie utworu.
     * @event stream_audio
     */
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

    /**
     * Przechwytywanie prośby z serwera o wylistowanie aktualnych graczy.
     * @event list_players
     */
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

    /**
     * Przechwytywanie wiadomości z serwera oraz jej wyświetlanie jako komunikat.
     * @event server_info
     */
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

    /**
     * Przychwytuje wydarzenie 'start_game' z serwera.
     * @event start_game
     */
    socket.on("start_game", () => {
        startButton.style.display = "none";
        nextButton.style.display = "block";

        songsChoice.style.display = "none";
        mediaPlayer.style.display = "block";
    });

    /**
     * Przechwytuje wydarzenie 'Game Over' z serwera.
     * @event game_over
     */
    socket.on("game_over", () => {
        if (audioSource.src[0] != "h") {
            audioPlayer.currentTime += 15;
        }

        startButton.style.display = "block";
        nextButton.style.display = "none";

        songsChoice.style.display = "block";
        mediaPlayer.style.display = "none";
    });

    /**
     * Przechwytuje komunikat z serwera z prośbą o zaktualizowanie stanu pokoju.
     * @event click
     */
    socket.on("update_state", () => {
        startButton.style.display = "none";
        nextButton.style.display = "block";
        songsChoice.style.display = "none";
        mediaPlayer.style.display = "block";
    });

    /**
     * Wyślij wiadomość po kliknięciu przycisku 'send_message'.
     * @event click
     */
    document.querySelector("#send_message").onclick = () => {
        socket.send({"msg": document.querySelector("#user_message").value, "username": username, "room": room_name, "is_admin": is_admin});
        document.querySelector("#user_message").value = "";
    }

    /**
     * Rozpocznij nową rundę w przypadku kliknięcia przycisku 'Next Round'.
     * @event click
     */
    document.querySelector("#next_round_button").onclick = () => {
        socket.emit("request_audio", {"room": room_name});
    }

    /**
     * Zacznij grę kiedy przycisk 'Start' zostanie kliknięty.
     * @event click
     */
    startButton.onclick = () => {
        cathegory = songsChoice.value
        socket.emit('start', {"room": room_name, "cathegory": cathegory});
    }

    /**
     * Wysyła informację do serwera o opuszczeniu pokoju.
     * @function
     */
    function leaveRoom() {
        socket.emit("leave", {"username": username, "room": room});
    }

    /**
     * Dołącz do pokoju i zaktualizuj jego stan.
     * @function
     */
    function joinRoom() {
        socket.emit("join", {"username": username, "room": room_name});
        socket.emit("update_state", {"room": room_name});
    }

    /**
     * Wyświetla wiadomości systemowe na czacie.
     * @function
     * @param {string} msg - Wiadomość do wyświetlenia.
     */
    function printSysMsg(msg) {
        const p = document.createElement("p");
        p.innerHTML = msg;
        p.style = "font-size: 1rem;";
        document.querySelector("#messages_area").append(p);
    }

});