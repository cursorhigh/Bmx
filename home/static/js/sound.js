function playHoverSound() {
    var hoverAudio = document.getElementById('hoverAudio');
    hoverAudio.play();
}

// Function to play click sound
function playClickSound() {
    var clickAudio = document.getElementById('clickAudio');
    clickAudio.play();
}

// Attach event listeners to buttons
var buttons = document.getElementsByClassName('hover-sound-button');
for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('mouseover', playHoverSound);
    buttons[i].addEventListener('click', playClickSound);
}