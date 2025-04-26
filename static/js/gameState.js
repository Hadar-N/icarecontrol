function parseFromFlaskJson(str) {
    return JSON.parse(str.replaceAll(/(&#34;)|(&#39;)|(&lt;)|(&gt;)/g, '"').replaceAll("None", "null"));
}

const GameState = (function () {
    let consts = {};
    let strings = {};
    let curr_mode = null;
    let curr_level = null;
    let click_audio = new Audio('/static/audio/click.mp3');

    return {
        getConsts: () => {
            if (!consts) {
                throw new Error("consts not yet fetched!")
            }
            else return consts
        },
        setConsts: (str) => {
            consts = parseFromFlaskJson(str)
        },
        getStrings: () => {
            if (!strings) {
                throw new Error("strings not yet fetched!")
            }
            else return strings
        },
        setStrings: (str) => {
            strings = parseFromFlaskJson(str)
        },
        setCurrMode: (str) => curr_mode = str,
        getCurrModeStr: () => curr_mode ? strings["gamestart.html"].mode.options[curr_mode] : null,
        setCurrLevel: (str) => curr_level = str,
        getCurrLevelStr: () => curr_level ? strings["gamestart.html"].level.options[curr_level] : null,
        playClickAudio: () => {
            try {
                click_audio.play()
            } catch(err) {
                console.error("play error!", err)
            }
        }
    };
})();

window.GameState = GameState;