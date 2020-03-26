document.addEventListener('DOMContentLoaded', function () {
    const userName = JSON.parse(document.getElementById('userName').textContent),
        toastWrapper = document.getElementById('toast-wrapper'),
        toast = document.getElementById('toast'),
        messageInput = document.getElementById('message'),
        messageSubmit = document.getElementById('message__submit'),
        mention = document.getElementById('mention'),
        chatHistory = document.getElementById('chat-history');

    const updateToast = (val, mentioned, whoMentioned, timeout) => {  // could make same with triggering classes, but prefer control it better with JS
        if (mentioned === userName) {
            toast.innerHTML = `<span class="chat__message-mention__span">@${whoMentioned}:&nbsp;</span>${val}`;
            toastWrapper.style.transform = 'translateY(0) scale(1)';
            setTimeout(() => toastWrapper.style.transform = 'translateY(100%) scale(1, 0)', timeout)
        }
    };

    const messageTypeReducer = (jsonData) => {
        console.log(jsonData);
        let msgNode = document.createElement('p');
        msgNode.classList.add('chat__message');
        switch (jsonData['type']) {
            case 'mention':
                msgNode.classList.add('chat__mention');
                updateToast(jsonData['message'], jsonData['mentioned'], jsonData['username'], 8000);
                msgNode.innerHTML =
                    `<span class="chat__message__user">User: ${jsonData['username']}</span>
                        <span>
                        <span class="chat__message-mention__span">@${jsonData['mentioned']}:</span>
                                                ${jsonData['message']}
                        </span>
                    <span class="chat__message__time">Time: ${jsonData['time']}</span>`;
                break;
            case 'chat_message':
                msgNode.classList.add('message__default');
                msgNode.innerHTML =
                    `<span class="chat__message__user">User: ${jsonData['username']}</span>
                        ${jsonData['message']}
                    <span class="chat__message__time">Time: ${jsonData['time']}</span>`;
                break;
            case 'notification':
                msgNode.classList.add('chat__notification');
                msgNode.innerHTML =
                    `<span class="chat__message__user">User: ${jsonData['username']}</span>
                        ${jsonData['message']}
                    <span class="chat__message__time">Time: ${jsonData['time']}</span>`;
                break;
            default: throw new Error(`Unknown message type: ${jsonData['type']}`)
        }
        return msgNode
    };


    const handleSocket = url => {
        const chatSocket = new WebSocket(url);

        chatSocket.onmessage = e => {
            const data = JSON.parse(e.data);
            const newMessage = messageTypeReducer(data);
            chatHistory.prepend(newMessage);
        };

        chatSocket.onclose = () => {
            console.error('Chat socket closed unexpectedly');
        };

        messageInput.onkeyup = e => {
            if (e.key === 'Enter') {
                messageSubmit.click();
            }
        };

        messageSubmit.onclick = () => {

            if (!messageInput.value) {
                alert('Please, write your message');
                return
            }

            const messageType = mention.value ? 'mention' : 'chat_message';

            chatSocket.send(JSON.stringify({
                'username': userName,
                'message': messageInput.value,
                'message_type': messageType,
                'mentioned': mention.value || null
            }));
            messageInput.value = '';
            mention.value = ''
        };
    };

    const handleChat = () => {
        handleSocket(`ws://${window.location.host}/ws/chat/`)
    };

    handleChat()
});