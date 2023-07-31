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
    case "Suggestions":
        window.location.href = '/suggest'
    }
}