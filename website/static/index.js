copyButton = document.getElementById("copyToClipboard");

copyButton.onclick = function() {
    var copyText = document.getElementById("inviteLink").textContent;
    // alert("COPY:", copyText);
    // TODO: POPRAWIĆ TO!
    navigator.clipboard.writeText(copyText);
}