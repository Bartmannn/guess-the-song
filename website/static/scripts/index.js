/**
 * Reference to the 'Copy to Clipboard' button HTML element.
 * @type {HTMLElement}
 */
var copyButton = document.getElementById("copyToClipboard");

/**
 * Reference to the 'Next Round' button HTML element.
 * @type {HTMLElement}
 */
var nextRoundButton = document.getElementById("next_round_button");

/**
 * Reference to the 'Start Game' button HTML element.
 * @type {HTMLElement}
 */
var startGameButton = document.getElementById("start_game_button");


/**
 * Variable indicating the administrative status.
 * @type {boolean}
 */
console.log(is_admin);

/**
 * Add an onclick event listener to the 'Copy to Clipboard' button.
 * Copies the content of the 'invite_link' field to the clipboard.
 * @event click
 */
copyButton.onclick = () => {
    var copyText = document.getElementById("invite_link");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}


/**
 * Disable and apply grayscale filters to buttons if the user is not an admin.
 * @type {boolean}
 */
if (is_admin == "False") {
    startGameButton.style.filter = "grayscale(50%)";
    nextRoundButton.style.filter = "grayscale(75%)";
    startGameButton.disabled = true;
    nextRoundButton.disabled = true;
}