/**
 * HTML content representing the game room.
 * @type {string}
 */
const gameContent = "\
<h1>Room: "+ room_name +" - <span id='current_round'></span></h1>\
<div class='game_room'>\
    <div class='players'>\
        <h3>Hello, There!</h3>\
        <ol id='users_list'>\
        </ol>\
    </div>\
    <div class='game_board'>\
        <audio id='audioPlayer' autoplay>\
            <source src='' type='audio/mpeg' id='audioSource'>\
        </audio>\
    </div>\
    <div class='chat'>\
        <p>Messages</p>\
        <div id='messages_area'>\
        </div>\
        <input type='text' name='user_message' id='user_message'>\
        <button type='button' id='send_message'>Send</button>\
    </div>\
</div>\
<textarea id='inviteLink' style='display: none;'>"+ invite_link +"</textarea>\
<input type='button' id='copyToClipboard' value='Copy invite link to clipboard'>\
<input type='button' style='display: none;' id='start_game_button' value='Start'>\
<input type='button' style='display: block;' id='next_round_button' value='Next'>\
"

/**
 * HTML content representing the configuration view of the room.
 * @type {string}
 */
const configContent = "\
<h1>Room: "+ room_name +"</h1>\
    <div class='game_room'>\
        <div class='players'>\
            <h3>Hello, There!</h3>\
            <ol id='users_list'>\
            </ol>\
        </div>\
        <select name='songs' id='songs'>\
            <option value='popular'>Utwory popularne w Polsce</option>\
            <option value='all'>Wszystko</option>\
            <option value='films'>Filmy</option>\
            <option value='games'>Gry</option>\
        </select>\
        <div class='chat'>\
            <p>Messages</p>\
            <div id='messages_area'>\
            </div>\
            <input type='text' name='user_message' id='user_message'>\
            <button type='button' id='send_message'>Send</button>\
        </div>\
    </div>\
    <input type='button' id='copyToClipboard' onclick='copy_invite_link()' value='Invite'>\
    <input type='button' style='display: block;' id='start_game_button' value='Start'>\
<input type='button' style='display: none;' id='next_round_button' value='Next'>\
"

/**
 * HTML content representing a configuration section with a dropdown for song selection.
 * @type {string}
 */
const config = "\
<select name='songs' id='songs'>\
    <option value='popular'>Utwory popularne w Polsce</option>\
    <option value='all'>Wszystko</option>\
    <option value='films'>Filmy</option>\
    <option value='games'>Gry</option>\
</select>\
"

/**
 * HTML content representing an audio player for music playback.
 * @type {string}
 */
const music = "\
<audio id='audioPlayer' autoplay>\
    <source src='' type='audio/mpeg' id='audioSource'>\
</audio>\
"

document.getElementById("room_content").innerHTML = config;