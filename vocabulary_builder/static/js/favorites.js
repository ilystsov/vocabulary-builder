// favorites.js

function fetchAndDisplayFavorites() {
    const accessToken = getCookie('access_token');
    if (!accessToken) {
        console.error('Access token is not found in cookies.');
        return;
    }

    const decodedToken = decodeJWT(accessToken.split(' ')[1]);
    const userId = decodedToken.user_id;

    if (!userId) {
        console.error('User ID is not found in the token.');
        return;
    }

    fetch(`/users/${userId}/words`)
        .then((response) => response.json())
        .then((data) => {
            const wordCardContainer = document.getElementById(
                'favorites-card-container',
            );
            const noWordsMessage = document.getElementById('no-words-message');

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

            if (data.length !== 0) {
                noWordsMessage.style.display = 'none';
                data.forEach((wordData) => {
                    const wordCard = createWordCard(wordData, language);
                    wordCardContainer.appendChild(wordCard);
                });

                const msnry = new Masonry(wordCardContainer, {
                    itemSelector: '.word-card',
                    columnWidth: '.word-card',
                    gutter: 16,
                    fitWidth: true,
                });
                imagesLoaded(wordCardContainer, function () {
                    msnry.layout();
                });
            }
        })
        .catch((error) => {
            console.error('Error fetching favorite words:', error);
        });
}

document.addEventListener('DOMContentLoaded', fetchAndDisplayFavorites);
