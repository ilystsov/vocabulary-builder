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
    if (!checkRegistration()) {
        return;
    }
}

function welcomeTestingFeature() {
    if (!checkRegistration()) {
        return;
    }
}

function getWelcomeNewWordCard() {
    // FETCH

    const wordCardContainer = document.getElementById(
        'word-card-welcome-container',
    );
    wordCardContainer.style.display = 'block';

    scrollToWelcomeNewWord();
}

// Modal
function showModal() {
    const modal = document.getElementById('registration-modal');
    modal.style.display = 'block';
    document.body.classList.add('modal-active');
    return false;
}

function closeModal() {
    const modal = document.getElementById('registration-modal');
    modal.style.display = 'none';
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
