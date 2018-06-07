window.onload = function () {

    let chatHistory = document.querySelector('#chat-history'),
        descendants = chatHistory.getElementsByTagName('p');
    for(let i = 0; i < descendants.length; i++) {
        someDiv = descendants[i];

        if(someDiv.getAttribute('class') === 'msg_text') {
            someDiv.addEventListener("click", function (event) {
                copyAndPlay(event.target.innerText);
                // console.log(event.target.innerText);
            });
        }
    }

    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    let chatSocket = new ReconnectingWebSocket(
        ws_scheme + '://' +
        window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function(e) {
        console.log('inside onmessage');
        let data = JSON.parse(e.data),
            message = data['message'];
        let sender = data['sender'],
            firstName = data['first_name'],
            lastName = data['last_name'],
            timestamp = JSON.parse(data['timestamp']);

        let newDiv = document.createElement('div');

        let requiredClass = 'one_message ' + ((sender === currentUsername) ? 'sent': 'received');
        newDiv.setAttribute('class', requiredClass);
        newDiv.innerHTML += '<p class="sender_name">' + firstName + ' ' + lastName + ' ' + timestamp + '</p>';
        newDiv.setAttribute('id',timestamp.toString().replace(/\s/g,''));
        newDiv.innerHTML += '<hr>';
        newDiv.innerHTML += '<p class="msg_text">' + message + '</p>';
        newDiv.addEventListener('click', function () {
            copyAndPlay(newDiv.querySelector('.msg_text').innerText);
            // console.log(newDiv.querySelector('.msg_text').innerText);
        });

        document.querySelector('#chat-history').appendChild(newDiv);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#s1').focus();
    document.querySelector('#s1').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        console.log('inside onclick');
        let messageInputDom = document.querySelector('#s1'),
            message = messageInputDom.value,
            roomLabel = document.querySelector('#current_room_label').getAttribute('value'),
            sender = document.querySelector('#sender').getAttribute('value');

        chatSocket.send(JSON.stringify({
            'message': message,
            'room_label': roomLabel,
            'sender': sender
        }));

        messageInputDom.value = '';
    };
};

function copyAndPlay(text) {
    let textArea = document.querySelector('#s1');
    s1.value = text.toLowerCase();
//    console.log(s1.value);
    piano.recplay();
}