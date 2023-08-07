$(document).ready(function() {
  const currentUsername = getQueryParam('username');
  const chatInput = document.getElementById('chatInput');
  const sendMsgButton = document.getElementById('sendMsgButton'); 
  function scrollToBottom() {
    const msgbox = document.querySelector('.msgbox');
    msgbox.scrollTop = msgbox.scrollHeight;
  } 
  chatInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      sendmsg();
      scrollToBottom(); 
      event.preventDefault();
    }
  });
  sendMsgButton.addEventListener('click', function() {
    sendmsg(); 
    scrollToBottom();
  });

  // Function to handle sending messages
  function sendmsg() {
    const messageText = chatInput.textContent.trim();
    if (messageText === '') {
      return;
    }

    socket.send(JSON.stringify({ message: messageText }));

    chatInput.textContent = '';

    const newMessage = document.createElement('div');
    newMessage.textContent = messageText;
    newMessage.classList.add('sender-message');

    const usernameElement = document.createElement('div');
    usernameElement.textContent = 'you';
    usernameElement.classList.add('yusername');

    const messageContainer = document.createElement('div');
    messageContainer.appendChild(usernameElement);
    messageContainer.appendChild(newMessage);
    messageContainer.classList.add('mine-container');

    const msgbox = document.querySelector('.msgbox');
    msgbox.appendChild(messageContainer);
  }
  socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const messageType = data.type;
    if (messageType === 'chat_history') {
      handleChatHistory(data, currentUsername);
      scrollToBottom();
    } else {
      const username = data.username;
      const message = data.message;

      const usernameElement = document.createElement('div');
      usernameElement.textContent = username;
      usernameElement.classList.add('username');
    
      const messageElement = document.createElement('div');
      messageElement.textContent = message;
      messageElement.classList.add('message');
    
      const messageContainer = document.createElement('div');
      messageContainer.appendChild(usernameElement);
      messageContainer.appendChild(messageElement);
      messageContainer.classList.add('other-container');

      const msgbox = document.querySelector('.msgbox');
      msgbox.appendChild(messageContainer);
      scrollToBottom();
    }
  };
});


function handleChatHistory(data, currentUsername) {
  const username = data.username;
  const message = data.message;
  const usernameElement = document.createElement('div');
  const messageElement = document.createElement('div');
  messageElement.textContent = message;
  const messageContainer = document.createElement('div');
  messageContainer.appendChild(usernameElement);
  messageContainer.appendChild(messageElement);
  if (username === currentUsername) {
    usernameElement.textContent = 'you';
    usernameElement.classList.add('yusername'); 
    messageElement.classList.add('sender-message');
    messageContainer.classList.add('mine-container');
  } else {
    usernameElement.classList.add('username');
    messageElement.classList.add('message');
    usernameElement.textContent = username;
    messageContainer.classList.add('other-container');
  }

  const msgbox = document.querySelector('.msgbox');
  msgbox.appendChild(messageContainer);
}


let username = getQueryParam('username')
function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}
let url = `ws://${window.location.host}/ws/globalchat/${username}/`;
let socket = new WebSocket(url);
socket.onopen = function(event) {
    console.log('Connected to GlobalChat',username);
};
function handleButtonClick(buttonTitle) {
  switch (buttonTitle) {
  case "Back To Home":
      window.location.href = '/';
      break;
  }
}
