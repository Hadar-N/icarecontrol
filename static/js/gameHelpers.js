function parseFromFlaskJson(str) {
    return JSON.parse(str.replaceAll(/(&#34;)|(&#39;)|(&lt;)|(&gt;)/g,'"'));
}

function isEnglish(str) {
    return(str && !!str.match(/^[A-Za-z]/))
}

function clickControlFunc(elm, matched_list) {
    fetch('/publish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            command: elm.getAttribute("command"),
            matched: matched_list
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.redirect) window.location.href = data.redirect;
        })
}

function speakWord(str) {
    fetch('/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            word: str
        })
    })
}

function createSpeakerButton(str) {
    const svg = document.createElement('img');
    svg.src = "/static/icons/speaker.svg";
    svg.alt = "speaker";
    svg.id = `sp-${str}`
    svg.onclick = () => speakWord(str);
    return svg;
}

function createListItem(str) {
    const li = document.createElement('li');
    li.id = `l-${str}`
    const is_english = isEnglish(str)
    const div = document.createElement('div');
    div.textContent = str;
    is_english && div.prepend(createSpeakerButton(str))
    li.appendChild(div);
    is_english && speakWord(str)
    return li;
}

function finishGame(new_stat, matched_list) {
    fetch('/savesession', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            status: new_stat,
            matched: matched_list
        })
    }).then(() => window.location.href = '/game/end');
}

function messageEffects(msg_list, list_elm, matched_list) {
    let new_status = false;
    const actions = GameState.getConsts().MQTT_DATA_ACTIONS
    for (let i of msg_list) {
        switch (i.type) {
            case actions.NEW:
                if (i.word.word && typeof i.word.word === "string") list_elm.prepend(createListItem(i.word.word));
                break;
            case actions.REMOVE:
                document.getElementById(`l-${i.word.word}`).remove();
                break;
            case actions.MATCHED:
                document.getElementById(`l-${i.word.word}`).classList.add("matched");
                if(isEnglish(i.word.word)) document.getElementById(`sp-${i.word.word}`).disabled = true; // TODO: fix
                matched_list.push(i.word);
                break;
            case actions.STATUS:
                new_status = i.word;
                break;
            default:
                console.error("type non valid!", i);
        }
    }
    return new_status;
}

function titleBasedOnStatus(status) {
    let res = '';
    const statuses = GameState.getConsts().GAME_STATUS
    switch(status) {
        case statuses.DONE:
            res = '<b>congratulations!</b><br />game finished!'
            break;
        case statuses.ACTIVE:
            break;
        case statuses.HALTED:
            res = '<b>Oh no!</b><br />game stopped'
            break;
        default:
            console.error('unrecognized game status!', status)
            res = '<b>Game encountered issues...'
    }
    return res;
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

changeStageStyle = (elms, field_names, prev_stage_i, curr_stage_i) => {
    if (prev_stage_i !== curr_stage_i) {
        for (elm of elms) {
            if (elm.id === field_names[curr_stage_i]) {
                elm.style.opacity= 1
                elm.classList.remove('slide-right', 'slide-left')
            } else if (elm.id === field_names[prev_stage_i] || !prev_stage_i && field_names.slice(0,curr_stage_i).includes(elm.id)) {
                elm.classList.add(prev_stage_i < curr_stage_i || !prev_stage_i ? 'slide-left' : 'slide-right')
            } else if (!prev_stage_i) {
                elm.style.opacity= 0
                elm.classList.add('slide-right')
            }
        }
    }
}

displayIfNotInitial = (elm, stage) => {
    if (!!stage) elm.style.display = 'block'
    else elm.style.display = 'none'
}
