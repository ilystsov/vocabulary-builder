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
            wordCardContainer.innerHTML = ''; // Clear previous cards
            data.forEach((wordData) => {
                const wordCard = createWordCard(wordData, 'ru'); // Assuming 'ru' is the default language
                wordCardContainer.appendChild(wordCard);
            });

            adjustCardLayout();
        })
        .catch((error) =>
            console.error('Error fetching favorite words:', error),
        );
}

function adjustCardLayout() {
    var COL_COUNT = 4; // set this to however many columns you want
    var col_heights = [],
        container = document.getElementById('favorites-card-container');
    for (var i = 0; i <= COL_COUNT; i++) {
        col_heights.push(0);
    }

    for (var i = 0; i < container.children.length; i++) {
        var order = (i + 1) % COL_COUNT || COL_COUNT;
        container.children[i].style.order = order;
        col_heights[order] += parseFloat(container.children[i].clientHeight);
    }

    var highest = Math.max.apply(Math, col_heights);
    container.style.height = highest + 'px';
}

document.addEventListener('DOMContentLoaded', fetchAndDisplayFavorites);
