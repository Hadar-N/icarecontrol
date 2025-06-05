function printInPythonTerminal(str) {
    console.log(str)
    fetch('/print_to_terminal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ str })
    })
}

function clickControlFunc(command, payload= null) {
    fetch('/publish_command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, payload })
    })
        .then(res => res.json())
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
