function changeLanguage(language) {
    var url;
    if (language === 'ru') {
        url = '/';
    } else {
        url = '/' + language;
    }
    window.location.href = url;
}