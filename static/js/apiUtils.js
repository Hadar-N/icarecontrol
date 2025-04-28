function printInPythonTerminal(str) {
    fetch('/print_to_terminal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ str })
    })
}

function clickControlFunc(command) {
    fetch('/publish_command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
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

function selectOptions(word, opt) {
    fetch('/publish_select', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            word,
            selected: opt
        })
    })
}

function startGame(mode, level) {
    fetch('/start_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            mode,
            level
        })
    })
}
