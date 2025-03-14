function parseFromFlaskJson(str) {
    return JSON.parse(str.replaceAll(/(&#34;)|(&#39;)|(&lt;)|(&gt;)/g,'"'));
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
    li.id = `w-${str}`
    const div = document.createElement('div');
    div.textContent = str;
    div.prepend(createSpeakerButton(str))
    li.appendChild(div);
    speakWord(str)
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
    for (let i of msg_list) {
        console.log("messageEffects", i)
        switch (i.type) {
            case window.APP_CONSTANTS.MQTT_DATA_ACTIONS.NEW:
                if (i.word.en && typeof i.word.en === "string") list_elm.prepend(createListItem(i.word.en));
                break;
            case window.APP_CONSTANTS.MQTT_DATA_ACTIONS.REMOVE:
                document.getElementById(`w-${i.word.en}`).remove();
                break;
            case window.APP_CONSTANTS.MQTT_DATA_ACTIONS.MATCHED:
                document.getElementById(`w-${i.word.en}`).classList.add("matched");
                document.getElementById(`sp-${i.word.en}`).disabled = true; // TODO: fix
                matched_list.push(i.word);
                break;
            case window.APP_CONSTANTS.MQTT_DATA_ACTIONS.STATUS:
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
    switch(status) {
        case window.APP_CONSTANTS.GAME_STATUS.DONE:
            res = '<b>congratulations!</b><br />game finished!'
            break;
        case window.APP_CONSTANTS.GAME_STATUS.ACTIVE:
            break;
        case window.APP_CONSTANTS.GAME_STATUS.HALTED:
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
