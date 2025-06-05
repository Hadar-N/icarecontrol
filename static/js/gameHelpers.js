function isEnglishMode() {
    return GameState.getCurrModeStr() && !!GameState.getCurrModeStr().match(/英文/)
}
function isSpellingMode() {
    return GameState.getCurrModeStr() && !!GameState.getCurrModeStr().match(/拼寫/)
}

function createSpeakerButton(str, add_onclick = true) {
    const svg = document.createElement('img');
    svg.src = "/static/icons/speaker.svg";
    svg.alt = "speaker";
    svg.classList.add('mini-img')
    svg.classList.add('spkr-img')
    svg.id = `sp-${str}`
    if(add_onclick) {
        svg.onclick = (e) => {
            e.stopPropagation()
            GameState.playClickAudio()
            speakWord(str)
        };
    }
    return svg;
}

function createListItem(str) {
    const li = document.createElement('li');
    li.id = `l-${str}`
    const is_english = !str.match(/[^A-Za-z1-9 \-]/)
    const div = document.createElement('div');
    div.classList.add('main-part')
    div.textContent = str;
    if (is_english) {
        div.prepend(createSpeakerButton(str))
    }
    li.appendChild(div);
    return li;
}

function supportListScrolling(div) {
    let isDown = false;
    let startY, scrollTop;

    const mousemovefunc = e => {
        const y = e.pageY - div.offsetTop;
        const walk = (y - startY) * 2;
        div.scrollTop = scrollTop - walk;
    }

    div.addEventListener('mousedown', (e) => {
        isDown = true;
        startY = e.pageY - div.offsetTop;
        scrollTop = div.scrollTop;
        div.addEventListener('mousemove', mousemovefunc)
    });

    div.addEventListener('mouseleave', () => {
        isDown = false;
        div.removeEventListener('mousemove', mousemovefunc)
    });

    div.addEventListener('mouseup', () => {
        isDown = false;
        div.removeEventListener('mousemove', mousemovefunc)
    });

}