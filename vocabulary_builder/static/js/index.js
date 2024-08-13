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

// Specific event listeners

function setupWelcomePageEventListeners() {
    // registration modal
    const closeRegistrationModalButton = document.getElementById(
        'close-registration-modal-button',
    );
    closeRegistrationModalButton.addEventListener(
        'click',
        closeRegistrationModal,
    );

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

    const favoritesFeature = document.getElementById('favorites-feature');
    favoritesFeature.addEventListener('click', () => {
        showRegistrationModal();
    });

    const testingFeature = document.getElementById('testing-feature');
    testingFeature.addEventListener('click', () => {
        showRegistrationModal();
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
    let language = getLanguageFromUrl();
    if (language) {
        localStorage.setItem('language', language);
    } else {
        language = localStorage.getItem('language') || 'ru';
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('language', language);
        const newUrl = `${window.location.pathname}?${urlParams.toString()}`;

        window.location.replace(newUrl);
    }
    console.log(language);

    document.body.classList.remove('hidden');

    // toggle theme
    const toggleThemeButton = document.getElementById('toggle-theme-button');
    toggleThemeButton.addEventListener('click', toggleTheme);

    if (document.body.classList.contains('welcome-page')) {
        setupWelcomePageEventListeners();
    } else {
        setupLearnPageEventListeners();
    }
});

function _(msgid) {
    return msgid;
}

document.addEventListener('DOMContentLoaded', function () {
    const changingText = document.getElementById('changing-text');
    const hiddenMessages = document.querySelectorAll('#hidden-messages p');

    const messages = Array.from(hiddenMessages).map((p) => p.textContent);

    let currentIndex = 0;

    function fadeInText(newText) {
        changingText.textContent = newText;
        changingText.classList.remove('fade-out');
        changingText.classList.add('fade-in');
    }

    function fadeOutText(callback) {
        changingText.classList.remove('fade-in');
        changingText.classList.add('fade-out');
        setTimeout(callback, 1000); // Wait 1 second for the animation to complete
    }

    let intervalId = setInterval(changeText, 8000);

    function changeText() {
        if (currentIndex < messages.length) {
            fadeOutText(() => {
                fadeInText(messages[currentIndex]);
                currentIndex += 1;
            });
        } else {
            clearInterval(intervalId); // Stop the loop after the last message
        }
    }
});
