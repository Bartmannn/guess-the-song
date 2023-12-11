// copyButton = document.getElementById("copyToClipboard");
startButton = document.getElementById("start_game_button");
nextButton = document.getElementById("next_round_button");
songsChoices = document.getElementById("songs");
mediaPlayer = document.getElementById("audioPlayer");

function copy(text) {
    // alert(text);
    navigator.clipboard.writeText(text);
}

startButton.onclick = function() {
    startButton.style.display = "none";
    nextButton.style.display = "block";

    songsChoices.style.display = "none";
    mediaPlayer.style.display = "block";
}

// copyButton.onclick = function() {
//     // var copyText = document.getElementById("inviteLink").textContent;
//     alert("COPY:", invite_link);
//     // TODO: POPRAWIĆ TO!
//     navigator.clipboard.writeText(invite_link);
//     // navigator.clipboard.writeText(inviteLink);
//     document.getElementById("copy_result").style.display = "block";
// }

