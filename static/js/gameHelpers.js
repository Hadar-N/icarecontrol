function clickControlFunc(elm) {
    fetch('/publish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: elm.getAttribute("command") })
    })
        .then(res => res.json())
        .then(data => {
            if (data.redirect) window.location.href = data.redirect;
        })
}

function createListItem(str) {
    const li = document.createElement('li');
    li.id = `w-${str}`
    li.textContent = str;
    const svg = document.createElement('img');
    svg.src = "/static/icons/speaker.svg";
    li.appendChild(svg)
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
                document.getElementById(`w-${i.word.en}`).remove()
                break;
            case window.APP_CONSTANTS.MQTT_DATA_ACTIONS.MATCHED:
                document.getElementById(`w-${i.word.en}`).classList.add("matched")
                matched_list.push(i.word)
                break;
            case window.APP_CONSTANTS.MQTT_DATA_ACTIONS.STATUS:
                new_status = i.word;
                break;
            default:
                console.error("type non valid!", i)
        }
    }
    return new_status;
}

function titleBasedOnStatus(status) {
    let res = '';
    switch(status) {
        case window.APP_CONSTANTS.MQTT_STATUSES.FINISHED:
            res = '<b>congratulations!</b><br />game finished!'
            break;
        case window.APP_CONSTANTS.MQTT_STATUSES.ONGOING:
            break;
        case window.APP_CONSTANTS.MQTT_STATUSES.STOPPED:
            res = '<b>Oh no!</b><br />game stopped'
            break;
        case window.APP_CONSTANTS.MQTT_STATUSES.ERROR:
            res = '<b>Game encountered issues...'
            break;
    }
    return res;
}
