document.getElementById('new-word-btn').addEventListener('click', async function() {
    const language = window.location.pathname.split('/')[1];
    const response = await fetch(`/${language}/new_word`);
    const data = await response.json();
    document.getElementById('word').textContent = data.word;
    document.getElementById('context').textContent = data.context;
    document.getElementById('translated_context').textContent = data.translated_context;
});
