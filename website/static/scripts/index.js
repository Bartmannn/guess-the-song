// copyButton = document.getElementById("copyToClipboard");
startButton = document.getElementById("start_game_button");

function copy(text) {
    // alert(text);
    navigator.clipboard.writeText(text);
}

startButton.onclick = () => {
    document.getElementById("content").innerHTML = music;
    document.getElementById("start_game_button").style.display = "none";
    document.getElementById("next_round_button").style.display = "block";
}

// copyButton.onclick = function() {
//     // var copyText = document.getElementById("inviteLink").textContent;
//     alert("COPY:", invite_link);
//     // TODO: POPRAWIĆ TO!
//     navigator.clipboard.writeText(invite_link);
//     // navigator.clipboard.writeText(inviteLink);
//     document.getElementById("copy_result").style.display = "block";
// }
