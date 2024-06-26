function toggleStar() {
    if (!checkRegistration()) {
        return;
    }

    const star = document.querySelector('.word-card__star');
    star.classList.toggle('word-card__star--active');
}
