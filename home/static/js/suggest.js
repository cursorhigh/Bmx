function handleButtonClick(buttonTitle) {
    switch (buttonTitle) {
    case "Suggest Changes":
        window.location.href = 'https://forms.gle/rnauCCDUG5bDgo9V6';
        break;
    case "Submit Quiz":
        window.location.href = 'https://forms.gle/Zo26AkfJuC4wPgz6A';
        break;
    case "Report Bugs":
        window.location.href = 'https://forms.gle/cvmRA4GXwbbiyDQe8';
        break;
    case "Back To Settings":
        window.location.href = '/settings';
        break;
    }
}