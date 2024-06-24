document.getElementById('new-word-btn').addEventListener('click', function () {
    const language =
        new URLSearchParams(window.location.search).get('language') || 'ru';
    fetch(`/new_word?language=${language}`)
        .then((response) => response.json())
        .then((data) => {
            document.getElementById('word').textContent = data.word;
            document.getElementById('context').textContent = data.context;
            document.getElementById('translated_context').textContent =
                data.translated_context;
        });
});
