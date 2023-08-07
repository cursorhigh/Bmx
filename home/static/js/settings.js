function handleButtonClick(buttonTitle) {
    switch (buttonTitle) {
    case "Back To Home":
        window.location.href = '/';
        break;
    case "Reset":
        if (confirm("Are you sure you want to reset the score?")) {
            window.location.href = '/reset';
        }
        break;
    case "Permanent Account Delete":
        if (confirm("Are you sure you want to permanently delete your account (not undoable)?")) {
            sendPostRequest('/permanentdelete/');
        }
        console.log('done')
        break;
    case "Suggestions":
        window.location.href = '/suggest'
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}   
function sendPostRequest(url) {
    const csrftoken = getCookie('csrftoken');
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                // Redirect after successful deletion
                window.location.href = '/';
            } else {
                // Handle error if needed
                console.log('Error occurred during account deletion.');
            }
        }
    };
    xhttp.open('POST', url, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.setRequestHeader('X-CSRFToken', csrftoken);
    xhttp.send();
}
$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
    $('.reset-button').on('click', function() {
        handleButtonClick("Reset");
    });
    $('.suggest-button').on('click', function() {
        handleButtonClick("Suggestions");
    });
    $('.accdel-button').on('click', function() {
        handleButtonClick("Permanent Account Delete");
    });
    $('.back-button').on('click', function() {
        handleButtonClick("Back To Home");
    });
});
