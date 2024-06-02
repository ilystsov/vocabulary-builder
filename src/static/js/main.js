document.getElementById('new-word-btn').addEventListener('click', async function() {
    const response = await fetch('/new_word');
    const data = await response.json();
    document.getElementById('word').textContent = data.word;
    document.getElementById('context').textContent = data.context;
    document.getElementById('translated_context').textContent = data.translated_context;
});
