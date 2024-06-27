function createWordCard(data, language) {
    const wordCard = document.createElement('div');
    wordCard.className = 'word-card simple-box clickable shine-shift';

    const header = document.createElement('div');
    header.className = 'word-card__header';

    const wordContainer = document.createElement('div');
    wordContainer.className = 'word-card__word-container';
    const wordSpan = document.createElement('span');
    wordSpan.className = 'word-card__word';
    wordSpan.textContent = data.word;
    wordContainer.appendChild(wordSpan);

    const starDiv = document.createElement('div');
    starDiv.className = 'word-card__star';
    starDiv.setAttribute('onclick', 'toggleStar()');
    wordContainer.appendChild(starDiv);

    header.appendChild(wordContainer);

    const partOfSpeech = document.createElement('span');
    partOfSpeech.className = 'word-card__part-of-speech';
    partOfSpeech.textContent = data.part_of_speech;
    header.appendChild(partOfSpeech);

    const transcriptionAudio = document.createElement('div');
    transcriptionAudio.className = 'word-card__transcription-audio';
    const transcription = document.createElement('span');
    transcription.className = 'word-card__transcription';
    transcription.textContent = data.transcription;
    transcriptionAudio.appendChild(transcription);

    const audioButton = document.createElement('button');
    audioButton.classList.add('icon-button', 'word-card__audio-button');
    audioButton.setAttribute('onclick', 'playAudio()');
    const audioIcon = document.createElement('i');
    audioIcon.className = 'fas fa-volume-up';
    audioButton.appendChild(audioIcon);
    transcriptionAudio.appendChild(audioButton);

    header.appendChild(transcriptionAudio);
    wordCard.appendChild(header);

    const dividerHeader = document.createElement('div');
    dividerHeader.className = 'word-card__divider word-card__divider--header';
    wordCard.appendChild(dividerHeader);

    const content = document.createElement('div');
    content.className = 'word-card__content';

    const meaningsList = document.createElement('ol');
    meaningsList.className = 'word-card__meanings-list';

    data.semantics.forEach((semantic, index) => {
        const meaningBlock = document.createElement('li');
        meaningBlock.className = 'word-card__meaning-block';

        const meaning = document.createElement('div');
        meaning.className = 'word-card__meaning';
        meaning.textContent = semantic.translations[language].word;
        meaningBlock.appendChild(meaning);

        const examplesLabel = document.createElement('div');
        examplesLabel.className = 'word-card__examples-label';
        examplesLabel.textContent = getSpecialTranslation('examples');
        meaningBlock.appendChild(examplesLabel);

        const examplesList = document.createElement('ul');
        examplesList.className = 'word-card__examples-list';

        semantic.examples.forEach((example, exampleIndex) => {
            const exampleItem = document.createElement('li');

            const exampleText = document.createElement('p');
            exampleText.className = 'word-card__example';
            exampleText.textContent = example;
            exampleItem.appendChild(exampleText);

            const exampleTranslation = document.createElement('p');
            exampleTranslation.className = 'word-card__example-translation';
            exampleTranslation.textContent =
                semantic.translations[language].examples[exampleIndex];
            exampleItem.appendChild(exampleTranslation);

            examplesList.appendChild(exampleItem);
        });

        meaningBlock.appendChild(examplesList);
        meaningsList.appendChild(meaningBlock);

        if (index < data.semantics.length - 1) {
            const dividerMeaning = document.createElement('div');
            dividerMeaning.className =
                'word-card__divider word-card__divider--meaning';
            meaningsList.appendChild(dividerMeaning);
        }
    });

    content.appendChild(meaningsList);
    wordCard.appendChild(content);

    return wordCard;
}

function playAudio() {
    console.log('Play audio');
}

function toggleStar() {
    console.log('Toggle star');

    if (!checkRegistration()) {
        return;
    }

    const star = document.querySelector('.word-card__star');
    star.classList.toggle('word-card__star--active');
}

function fetchAndDisplayWordCard(callback) {
    const language =
        new URLSearchParams(window.location.search).get('language') || 'ru';
    const newWordButton = document.getElementById('get-new-word-button');
    const loadingIndicator = document.getElementById(
        'word-card-loading-indicator',
    );
    const wordCardContainer = document.getElementById('word-card-container');

    newWordButton.disabled = true; // Disable the button
    loadingIndicator.classList.remove('hidden'); // Show loading indicator
    wordCardContainer.classList.add('hidden'); // Hide word card container

    fetch(`/new_word?language=${language}`)
        .then((response) => response.json())
        .then((data) => {
            wordCardContainer.innerHTML = ''; // Clear previous word card
            const wordCard = createWordCard(data, language);
            wordCardContainer.appendChild(wordCard);
            if (callback) {
                callback(data);
            }
        })
        .catch((error) => console.error('Error fetching word data:', error))
        .finally(() => {
            wordCardContainer.classList.remove('hidden'); // Show word card container
            loadingIndicator.classList.add('hidden'); // Hide loading indicator
            newWordButton.disabled = false; // Enable the button
        });
}
