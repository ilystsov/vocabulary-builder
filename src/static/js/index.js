function toggleTheme() {
    return;
}

// Welcome functions
function scrollToWelcomeNewWord() {
    const wordSectionWelcome = document.getElementById('word-section-welcome');
    wordSectionWelcome.scrollIntoView({ behavior: 'smooth' });
}

function welcomeNewWordFeature() {
    scrollToWelcomeNewWord();

    const button = document.getElementById('new-word-welcome-button');
    highlightButton(button);
}

function welcomeFavouriteFeature() {
    return;
}

function welcomeTestingFeature() {
    return;
}

function getWelcomeNewWordCard() {
    // FETCH

    const wordCardContainer = document.getElementById(
        'word-card-welcome-container',
    );
    wordCardContainer.style.display = 'block';

    scrollToWelcomeNewWord();
}

// ==============

function highlightButton(button) {
    button.classList.add('highlight');

    setTimeout(() => {
        button.classList.remove('highlight');
    }, 300);
}

function redirectToSignUp() {
    window.location.href = '/signup';
}

function redirectToLogIn() {
    window.location.href = '/login';
}
