function toggleTheme() {
    return;
}

function welcomeNewWordFeature() {
    return;
}

function welcomeFavouriteFeature() {
    return;
}

function welcomeTestingFeature() {
    return;
}

function scrollToWelcomeNewWord() {
    const wordSectionWelcome = document.getElementById('word-section-welcome');
    wordSectionWelcome.scrollIntoView({ behavior: 'smooth' });
}

function getWelcomeNewWordCard() {
    // FETCH

    const wordCardContainer = document.getElementById(
        'word-card-welcome-container',
    );
    wordCardContainer.style.display = 'block';

    scrollToWelcomeNewWord();
}

function redirectToSignUp() {
    window.location.href = '/signup';
}

function redirectToLogIn() {
    window.location.href = '/login';
}
