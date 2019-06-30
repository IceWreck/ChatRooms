document.addEventListener('DOMContentLoaded', () => {

    // Init
    // ---------------------------------------//    

    // Connect to a websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Set a default channel if last used channel doesn't exist and connect to it
    if (!localStorage.getItem("channel_name")) {
        localStorage.setItem("channel_name", 'Lounge');
    }
    let channel_name = localStorage.getItem("channel_name");
    document.querySelector("#channel-name").innerHTML = channel_name;

    // Chat Functionality
    // ---------------------------------------//

    /*
     *
     * There are two types of json emissions,
     * client_emit is the json emitted by javascript on the client's browser (in chat.js)
     * server_emit is the json emitted by python on the server (in app.py)
     *
     */

    // Implement send_message functionality
    socket.on('connect', () => {

        // Send message to server
        document.querySelector('#send_message').onclick = () => {
            message_text = document.querySelector('#input_message').value;
            socket.emit('client_emit', {
                'text': message_text,
                'channel': channel_name
            });
            // clear its value
            document.querySelector('#input_message').value = "";
        };
    });

    // Receive from server_emit and add message to page
    socket.on('server_emit', message_data => {
        // display message only if message's channel matches selected channel
        if (channel_name === message_data.channel) {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.innerHTML = `${message_data.text}`;
            document.querySelector('#chat').append(li);
            // scroll to bottom of page
            document.querySelector('#bottom-chat').scrollIntoView();
        }
    });


    // Other Tools
    // ---------------------------------------// 


    // Send message on pressing enter
    document.querySelector("#input_message").addEventListener("keyup", () => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector("#send_message").click();
        }
    });

    // Watch for channel change
    // TODO: convert this jquery syntax to pure JS
    $('#channel-list button').on('click', function () {
        channel_name = this.value;
        document.querySelector("#channel-name").innerHTML = channel_name;
        // remove messages from previous channel
        document.querySelector('#chat').innerHTML = "";
        // save this to local storage
        localStorage.setItem("channel_name", channel_name);
    });

});