/**
 * Odwołanie do przycisku 'Copy to Clipboard'.
 * @type {HTMLElement}
 */
var copyButton = document.getElementById("copyToClipboard");

/**
 * Odwołanie do przycisku 'Next Round'.
 * @type {HTMLElement}
 */
var nextRoundButton = document.getElementById("next_round_button");

/**
 * Odwołanie do przycisku 'Start Game'.
 * @type {HTMLElement}
 */
var startGameButton = document.getElementById("start_game_button");

/**
 * Wydarzenie zdefiniowane na przycisku 'Copy to Clipboard'.
 * Kopiuje zawartość pola 'invite_link'.
 * @event click
 */
copyButton.onclick = () => {
    var copyText = document.getElementById("invite_link");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}


/**
 * Wyłącza i aplikuje skalę szarości do przycisków, jeśli gracz nie jest adminem.
 * @type {boolean}
 */
if (is_admin == "False") {
    startGameButton.style.filter = "grayscale(50%)";
    nextRoundButton.style.filter = "grayscale(75%)";
    startGameButton.disabled = true;
    nextRoundButton.disabled = true;
}