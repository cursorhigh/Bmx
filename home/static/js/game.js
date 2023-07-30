let pid = getQueryParam('pid');
let roomname = getQueryParam('roomname');
let url = `ws://${window.location.host}/ws/game/${pid}/${roomname}/`;
function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}
let opponentConnected = false;
let socket = new WebSocket(url);
socket.onopen = function(event) {
    console.log('Connected to Game Server');
};
let countdownInterval;
const timerBar = document.querySelector('.timer-bar');
let redirectToHomepage = false;
function startTimer() {
    let timeLeft = 20; 
    countdownInterval = setInterval(() => {
      timeLeft -= 1;
      const percentage = (timeLeft / 20) * 100; 
      timerBar.style.width = percentage + '%';
  
      if (timeLeft <= 0) {
        clearInterval(countdownInterval);
        timerBar.style.width = '0%';
        requestNextQuestion();
      }
    }, 1000);
  }

  function resetTimer() {
    clearInterval(countdownInterval);
    timerBar.style.width = '100%';
  }

  function updateOpponentBikePosition(opponentScore) {
    const opponentBikeElement = document.getElementById('red-bike');
    const leftPosition = opponentScore * 0.9; // Increase left by 9% up to a maximum of 90%
    opponentBikeElement.style.left = leftPosition + '%';
  }
  function updateUserBikePosition(userScore) {
    const userBikeElement = document.getElementById('blue-bike');
    const leftPosition = userScore * 0.9; // Increase left by 9% up to a maximum of 90%
    userBikeElement.style.left = leftPosition + '%';
  }

socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'notify_disconnection') {
    alert(data.message);
    window.location.href = '/';
    } else if (data.type === 'opponent_connected') {
    console.log('Opponent connected');
    clearInterval(timerIntervals); 
    document.getElementById('timer-display').innerText = 'Opponent Connected';
    const opponentNameElement = document.getElementById('opponent-name');
    opponentNameElement.classList.add('player-connected');
    opponentConnected = true;
    } else if (data.type === 'opponent_id') {
    const opponentNameElement = document.getElementById('opponent-name');
    const category = document.getElementById('question-title');
    category.textContent = data.title;
    opponentNameElement.classList.add('player-connected');
    opponentNameElement.textContent = data.opponent_id;
    requestNextQuestion();
    } else if (data.type === 'question') {
        const questionContentElement = document.getElementById('question-content');
        const option1Element = document.getElementById('option-1');
        const option2Element = document.getElementById('option-2');
        const option3Element = document.getElementById('option-3');
        const option4Element = document.getElementById('option-4');
        const surrenderbutton = document.getElementById('surrender-button');
        const skipbutton = document.getElementById('skip-button');
        questionContentElement.textContent = data.question;

        option1Element.textContent = data.options[0];
        option2Element.textContent = data.options[1];
        option3Element.textContent = data.options[2];
        option4Element.textContent = data.options[3];

        option1Element.removeAttribute('disabled');
        option2Element.removeAttribute('disabled');
        option3Element.removeAttribute('disabled');
        option4Element.removeAttribute('disabled');
        surrenderbutton.removeAttribute('disabled');
        skipbutton.removeAttribute('disabled');
        resetTimer();
        startTimer();
    } else if (data.type === 'giveup') {
        redirectToHomepage = true;
        alert('You win! Opponent surrendered or Left the match.');
        window.location.href = '/';
    }  else if (data.type === 'update_player_score') {
        const playerScore = data.player_score;
        document.getElementById('player-score').textContent = 'Score: ' + playerScore;
        updateUserBikePosition(playerScore);
        requestNextQuestion();
    }
});
function requestNextQuestion() {
    if (opponentConnected) {
        socket.send(JSON.stringify({ type: 'request_question' }));
    }
}
function sAnswer(selectedOption) {
    var buttonId = 'option-' + selectedOption;
    var buttonText = document.getElementById(buttonId).textContent;
    socket.send(JSON.stringify({ type: 'submit_answer', option: buttonText }));
}
const timerDisplay = document.getElementById('timer-display');
let countdowns = 120; 

function updateTimerDisplay() {
    const minutes = Math.floor(countdowns / 60);
    const seconds = countdowns % 60;
    const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    timerDisplay.innerText = `waiting for opponent: ${formattedTime}`;
}

const timerIntervals = setInterval(() => {
    countdowns--;
    if (countdowns <= 0) {
    clearInterval(timerIntervals);
    }
    updateTimerDisplay();
}, 1000);


socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data.type === 'send.score') {
        var opponentScore = data.opponent_score;
        document.getElementById('opponent-score').innerText = 'Score: ' + opponentScore;
        updateOpponentBikePosition(opponentScore);
    } else if (data.type === 'game_results') {
        var winner = data.winner;
        var player1ID = data.player1_id;
        var player1Score = data.player1_score;
        var player2ID = data.player2_id;
        var player2Score = data.player2_score;
        alert('Game Over!\n: ' + winner + 
              '\n' + player1ID + ':' + player1Score +
              '\n' + player2ID + ':' + player2Score);
        redirectToHomepage = true;
        $.ajax({
            type: 'POST',
            url: '/update_score/',
            data: {
                'winner': winner,
                'player1_id': player1ID,
                'player1_score': player1Score,
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                console.log(response);
                window.location.href = '/';
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log(errorThrown);
                window.location.href = '/';
            }
        });
    } else if (data.type === 'player_left' && !redirectToHomepage) {
        var message = data.message;
        var winnerid = data.winnerid;
        var winnerscore = data.winnerscore;
        var youid = data.youid;
        var youscore = data.youscore;
        alert(message);
        $.ajax({
            type: 'POST',
            url: '/left_score/',
            data: {
                'winnerid': winnerid,
                'winnerscore': winnerscore,
                'youid': youid,
                'youscore': youscore
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                console.log(response);
                window.location.href = '/';
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log(errorThrown);
                window.location.href = '/';
            }
        });
    } else if (data.type === 'surrenderup') {
        var winnerid = data.winnerid;
        var winnerscore = data.winnerscore;
        var youid = data.youid;
        var youscore = data.youscore;
        $.ajax({
            type: 'POST',
            url: '/surrender_score/',
            data: {
                'winnerid': winnerid,
                'winnerscore': winnerscore,
                'youid': youid,
                'youscore': youscore
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                console.log(response);
                window.location.href = '/';
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log(errorThrown);
                window.location.href = '/';
            }
        });
    }  else if (data.type === 'game_over') {
        var gameOverLayer = document.getElementById('overlay');
        gameOverLayer.style.display = 'block';
    }
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



const surrenderButton = document.getElementById('surrender-button');
surrenderButton.addEventListener('click', () => {
    socket.send(JSON.stringify({ type: 'player_surrender' }));
});

const skipButton = document.getElementById('skip-button');
function updateSkipButtonText(skipCount) {
  skipButton.innerText = `Skip (${skipCount} skips left)`;
}

skipButton.addEventListener('click', () => {
  const currentSkipCount = parseInt(skipButton.innerText.match(/\d+/)[0]);
  if (currentSkipCount >=1) {
    const newSkipCount = currentSkipCount - 1;
    updateSkipButtonText(newSkipCount);
    socket.send(JSON.stringify({ type: 'player_skip' }));
  }
});

