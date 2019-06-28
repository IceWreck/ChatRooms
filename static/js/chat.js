document.addEventListener('DOMContentLoaded', () => {
    // Chat Functionality
    // ---------------------------------------//    
    // Connect to a websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Implement send_message functionality
    socket.on('connect', () => {

        // Send message to server
        document.querySelector('#send_message').onclick = () => {
            message_text = document.querySelector('#input_message').value;
            socket.emit('client_emit', {'text': message_text});
            // clear its value 
            document.querySelector('#input_message').value = "";
        };
    });

    // Add message to page
    socket.on('server_emit', message_data => {
        const li = document.createElement('li');
        li.innerHTML = `Wow: ${message_data.text}`;
        document.querySelector('#chat').append(li);
    });

    // ---------------------------------------// 
    // Other Tools
    
    // Send message on pressing enter 
    document.querySelector("#input_message").addEventListener("keyup", () => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector("#send_message").click();
        }
    });
});