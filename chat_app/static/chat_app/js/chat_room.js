document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('auth-form');

    const showChat = () => {
        const chat = document.getElementById('chat');
        chat.style.display = 'block';
        setTimeout(() => {
            chat.style.opacity = '1';
            chat.style.zIndex = '1';
            chat.querySelector('#message').focus()
        }, 500);
    };

    const hideAuth = () => {
        const chatAuthSection = document.getElementById('chat-authorize');
        chatAuthSection.style.opacity = '0';
        chatAuthSection.style.zIndex = '-1';
        setTimeout(() => chatAuthSection.style.display = 'none', 500);
    };

    const addUserName = val => {
        const title = document.getElementById('chat__title');
        title.innerText += `, ${val}!`
    };

    const handleSocket = (url, userName) => {
      const chatSocket = new WebSocket(url);

        chatSocket.onmessage = e => {
            const data = JSON.parse(e.data);
            const chatHistory = document.getElementById('chat-history');
            const newMessage = document.createElement('p');
            newMessage.classList.add('chat__message');
            data['type'] === 'notification' && newMessage.classList.add('chat__notification');

            newMessage.innerHTML =
                `<span class="chat__message__user">User: ${data['username']}</span>
                        ${data['message']}
                <span class="chat__message__time">Time: ${data['time']}</span>`;

            chatHistory.prepend(newMessage)
        };

        chatSocket.onclose = () => {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#message').onkeyup = e => {
            if (e.key === 'Enter') {
                document.querySelector('#message__submit').click();
            }
        };

        document.querySelector('#message__submit').onclick = () => {
            const messageInput = document.querySelector('#message');
            const message = messageInput.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
        };
    };

    const handleChat = userName => {
        hideAuth();
        showChat();
        addUserName(userName);
        handleSocket(`ws://${window.location.host}/ws/chat/${userName}/`)
    };

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const userName = document.getElementById('introduce').value;
        if (!userName) {
            alert('Please, provide valid username before continue chat.');
            return
        }
        handleChat(userName)
    })
});