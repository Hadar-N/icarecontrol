function updateText(elm_id, str) {
    document.getElementById(elm_id).textContent = str
}

function isEnglish(str) {
    return (str && !!str.match(/^[A-Za-z]/))
}

function clickControlFunc(elm, matched_list) {
    fetch('/publish_command', {
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
    svg.onclick = (e) => {
        e.stopPropagation()
        speakWord(str)
    };
    return svg;
}

function createChooseOptionBtn(str) {
    const div = document.createElement('div');
    div.id = `optionbtn-${str}`
    div.textContent = GameState.getStrings()['gameprocess.html'].options_btn
    div.classList.add('choose-option-btn')
    div.onclick = () => GameState.changeToggle(str)
    return div
}

function createListItem(str, options = []) {
    const li = document.createElement('li');
    li.id = `l-${str}`
    const is_english = isEnglish(str)
    const div = document.createElement('div');
    div.classList.add('main-part')
    div.textContent = str;
    if (is_english) {
        div.prepend(createSpeakerButton(str))
    }
    if (options.length) {
        div.append(createChooseOptionBtn(str))
    }
    li.appendChild(div);
    return li;
}

function messageEffects(msg, list_elm, matched_list, sounds) {
    const actions = GameState.getConsts().MQTT_DATA_ACTIONS
    switch (msg.type) {
        case actions.NEW:
            if (msg.word.word && typeof msg.word.word === "string" && !GameState.getWord(msg.word.word)) {
                GameState.addWord(msg.word)
                list_elm.prepend(createListItem(msg.word.word, msg.word.options));
                GameState.changeToggle(msg.word.word, true)
                if (isEnglish(msg.word.word)) speakWord(msg.word.word)
            }
            break;
        case actions.REMOVE:
            let existing_elm = document.getElementById(`l-${msg.word.word}`)
            if (GameState.isToggleOpen() && GameState.currToggleWord() == msg.word.word) GameState.changeToggle(msg.word.word, false) // TODO: fix
            if (existing_elm) existing_elm.remove();
            GameState.removeWord(msg.word)
            break;
        case actions.MATCHED:
            document.getElementById(`l-${msg.word.word}`).classList.add("matched");
            if (isEnglish(msg.word.word)) document.getElementById(`sp-${msg.word.word}`).disabled = true; // TODO: fix
            matched_list.push(msg.word);
            GameState.changeToggle(msg.word.word, false)
            sounds.success.play()
            break;
        case actions.STATUS:
            failed_match = GameState.getWord(msg.word.word)?.options.find(orig_op => {
                let found = msg.word.options.find(curr_opt => curr_opt.word === orig_op.word)
                return found.is_attempted !== orig_op.is_attempted
            })
            if (failed_match) {
                GameState.addWord(msg.word)
                if (GameState.isToggleOpen() && GameState.currToggleWord() == msg.word.word) GameState.changeToggle(msg.word.word, true)
                sounds.fail.play()
            }
            break;
        case actions.SELECT_FAIL:
            alert(GameState.getStrings()["gameprocess.html"].select_fail) // TODO: change alert to other mechanism! (or else the mqtt messages wont be received!!!)
        default:
            console.error("type non valid!", msg.type);
    }
}

const changePopUpContent = (title_elm, option_list_elm) => (str) => {
    obj = GameState.getWord(str);
    title_elm.textContent = obj.word;
    option_list_elm.innerHTML = "";
    for (let opt of obj.options) {
        item_elm = createListItem(opt.word)
        if (opt.is_attempted) item_elm.classList.add("fail-attempted");
        else {
            item_elm.classList.add('not-yet-attempted');
            item_elm.onclick = () => {
                if (isEnglish(opt.word)) speakWord(opt.word)
                fetch('/publish_select', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        word: obj.word,
                        selected: opt.word
                    })
                })
            }
        }
        option_list_elm.append(item_elm)
    }
}

function titleBasedOnStatus(status) {
    let res = '';
    res = GameState.getStrings()["gameend.html"].title?.[status]
    if (!res) {
        console.error('unrecognized game status!', status)
        res = GameState.getStrings()["gameend.html"].title.error
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
                elm.style.opacity = 1
                elm.classList.remove('slide-right', 'slide-left')
            } else if (elm.id === field_names[prev_stage_i] || !prev_stage_i && field_names.slice(0, curr_stage_i).includes(elm.id)) {
                elm.classList.add(prev_stage_i < curr_stage_i || !prev_stage_i ? 'slide-left' : 'slide-right')
            } else if (!prev_stage_i) {
                elm.style.opacity = 0
                elm.classList.add('slide-right')
            }
        }
    }
}

displayIfNotInitial = (elm, stage) => {
    if (!!stage) elm.style.display = 'block'
    else elm.style.display = 'none'
}
