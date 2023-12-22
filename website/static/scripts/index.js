// var startButton = document.getElementById("start_game_button");
// var nextButton = document.getElementById("next_round_button");
// var songsChoices = document.getElementById("songs");
// var mediaPlayer = document.getElementById("audioPlayer");
// var cathegory = ""
var copyButton = document.getElementById("copyToClipboard")

copyButton.onclick = () => {
    var copyText = document.getElementById("invite_link");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}

// function copy(text) {
//     navigator.clipboard.writeText(text);
// }

// startButton.onclick = () => {
//     console.log("CLI")

    // startButton.style.display = "none";
    // nextButton.style.display = "block";

    // songsChoices.style.display = "none";
    // mediaPlayer.style.display = "block";

//     cathegory = document.getElementById("songs").value
// }

// if (is_admin) {
//     startButton.disabled = true
// } else if (!is_admin) {
//     startButton.disabled = false
// }

