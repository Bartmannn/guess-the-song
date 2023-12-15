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

