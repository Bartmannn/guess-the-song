/**
 * Execute the following code after the DOM has been fully loaded.
 * @event DOMContentLoaded
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * Reference to the 'user_message' input field HTML element.
     * @type {HTMLInputElement}
     */
    let msg = document.querySelector("#user_message");

    /**
     * Add an event listener to the 'keyup' event for the 'user_message' input field.
     * @event keyup
     * @param {KeyboardEvent} event - The keyup event object.
     */

    msg.addEventListener("keyup", event => {
        /**
         * Key code for the "Enter" key.
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