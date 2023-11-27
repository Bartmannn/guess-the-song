copyButton = document.getElementById("copyToClipboard");

copyButton.onclick = function() {
    var copyText = document.getElementById("inviteLink").textContent;
    navigator.clipboard.writeText(copyText);
    
}