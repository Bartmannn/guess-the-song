/**
 * Wykonuje kod po pełnym załadowaniu strony.
 * @event DOMContentLoaded
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * Odwołanie do elementu HTML 'user_message'.
     * @type {HTMLInputElement}
     */
    let msg = document.querySelector("#user_message");

    /**
     * Dodanie wydarzenia na zwolnienie przycisku dla pola 'user_message'.
     * @event keyup
     * @param {KeyboardEvent} event - Obiekt wydarzenia.
     */

    msg.addEventListener("keyup", event => {
        /**
         * Kod przycisku entera.
         * @const
         * @type {number}
         */
        const enterKeyCode = 13;
        event.preventDefault();
        if (event.keyCode === enterKeyCode) {
            document.querySelector("#send_message").click();
        }
    })

});