var copyButton = document.getElementById("copyToClipboard");
var nextRoundButton = document.getElementById("next_round_button");
var startGameButton = document.getElementById("start_game_button");

console.log(is_admin);

copyButton.onclick = () => {
    var copyText = document.getElementById("invite_link");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}

if (is_admin == "False") {
    startGameButton.style.filter = "grayscale(50%)";
    nextRoundButton.style.filter = "grayscale(75%)";
    startGameButton.disabled = true;
    nextRoundButton.disabled = true;
}