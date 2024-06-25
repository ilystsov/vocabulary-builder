function toggleTheme() {
    return;
}

// Welcome functions
function scrollToWordSectionWelcome() {
    const wordSectionWelcome = document.getElementById('word-section-welcome');
    wordSectionWelcome.scrollIntoView({ behavior: 'smooth' });
}

function welcomeNewWordFeature() {
    scrollToWordSectionWelcome();

    const button = document.getElementById('new-word-button');
    highlightButton(button);
}

function welcomeFavouriteFeature() {
    if (!checkRegistration()) {
        return;
    }
}

function welcomeTestingFeature() {
    if (!checkRegistration()) {
        return;
    }
}

function fetchAndDisplayWordCardWelcome() {
    fetchAndDisplayWordCard();
    const wordCardContainer = document.getElementById('word-card-container');
    wordCardContainer.classList.remove('hidden');
}

// Modal
function showModal() {
    const modal = document.getElementById('registration-modal');
    modal.classList.remove('hidden');
    document.body.classList.add('modal-active');
}

function closeModal() {
    const modal = document.getElementById('registration-modal');
    modal.classList.add('hidden');
    document.body.classList.remove('modal-active');
}

// ==============

function highlightButton(button) {
    button.classList.add('highlight');

    setTimeout(() => {
        button.classList.remove('highlight');
    }, 300);
}

function checkRegistration() {
    // Replace this with actual registration check logic
    const isRegistered = false; // Example: false indicates the user is not registered

    if (!isRegistered) {
        return showModal();
    } else {
        return true;
    }
}

function redirectToSignUp() {
    window.location.href = '/signup';
}

function redirectToLogIn() {
    window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', function () {
    // for all pages
    fetchAndDisplayWordCard();
    document
        .getElementById('new-word-button')
        .addEventListener('click', fetchAndDisplayWordCard);

    // for welcome page
    if (document.body.classList.contains('welcome-page')) {
        document
            .getElementById('new-word-button')
            .addEventListener('click', fetchAndDisplayWordCardWelcome);
    }
});
