// import { fetchAndDisplayWordCard } from './word_card.js';

// Universal

function highlightButton(button) {
    button.classList.add('highlight');

    setTimeout(() => {
        button.classList.remove('highlight');
    }, 300);
}

// Common

function toggleTheme() {
    document.body.classList.toggle('gamma1');
    document.body.classList.toggle('gamma2');

    if (document.body.classList.contains('gamma2')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

function getSpecialTranslation(key) {
    const hiddenTranslations = document.getElementById('hidden-translations');
    const translationElement = hiddenTranslations.querySelector(
        `[data-key="${key}"]`,
    );
    return translationElement
        ? translationElement.textContent || translationElement.innerText
        : '';
}

// Registration modal

function showRegistrationModal() {
    const modal = document.getElementById('registration-modal');
    modal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
}

function closeRegistrationModal() {
    const modal = document.getElementById('registration-modal');
    modal.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
}

// Registration and log in

function checkRegistration() {
    // Replace this with actual registration check logic
    const isRegistered = false;

    if (!isRegistered) {
        return showRegistrationModal();
    } else {
        return true;
    }
}

// function redirectToSignUp() {
//     window.location.href = '/signup';
// }

// function redirectToLogIn() {
//     window.location.href = '/login';
// }

// Specific event listeners

function setupWelcomePageEventListeners() {
    const getNewWordButton = document.getElementById('get-new-word-button');
    getNewWordButton.addEventListener('click', () => {
        fetchAndDisplayWordCard(function (data) {
            console.log('Received data:', data);
            // Do smth with words' data
        });
        const wordCardContainer = document.getElementById(
            'word-card-container',
        );
        wordCardContainer.classList.remove('hidden');
    });

    const randomWordFeature = document.getElementById('random-word-feature');
    randomWordFeature.addEventListener('click', () => {
        getNewWordButton.scrollIntoView({ behavior: 'smooth' });
        highlightButton(getNewWordButton);
    });

    const favouritesFeature = document.getElementById('favourites-feature');
    favouritesFeature.addEventListener('click', () => {
        if (!checkRegistration()) {
            return;
        }
        // goto favourites
    });

    const testingFeature = document.getElementById('testing-feature');
    testingFeature.addEventListener('click', () => {
        if (!checkRegistration()) {
            return;
        }
        // goto testing
    });
}

function setupLearnPageEventListeners() {
    const getNewWordButton = document.getElementById('get-new-word-button');
    getNewWordButton.addEventListener('click', fetchAndDisplayWordCard);
}

function getLanguageFromUrl() {
    const currentPath = window.location.pathname;
    const urlParams = new URLSearchParams(window.location.search);
    let language = urlParams.get('language');
    if (!language && currentPath === '/') {
        language = 'ru';
    }
    return language;
}

// Event listeners

document.addEventListener('DOMContentLoaded', function () {
    // check theme
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.remove('gamma1');
        document.body.classList.add('gamma2');
    }

    // check language
    const language = getLanguageFromUrl();
    if (language) {
        localStorage.setItem('language', language);
    }
    console.log(language);

    document.body.classList.remove('hidden');

    // toggle theme
    const toggleThemeButton = document.getElementById('toggle-theme-button');
    toggleThemeButton.addEventListener('click', toggleTheme);

    // registration modal
    const closeRegistrationModalButton = document.getElementById(
        'close-registration-modal-button',
    );
    closeRegistrationModalButton.addEventListener(
        'click',
        closeRegistrationModal,
    );

    if (document.body.classList.contains('welcome-page')) {
        setupWelcomePageEventListeners();
    } else {
        setupLearnPageEventListeners();
    }
});
