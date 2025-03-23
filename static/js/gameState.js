function parseFromFlaskJson(str) {
    return JSON.parse(str.replaceAll(/(&#34;)|(&#39;)|(&lt;)|(&gt;)/g, '"').replaceAll("None", "null"));
}

const GameState = (function () {
    let consts = {};
    let strings = {};

    let toggled_elm= null;
    let is_toggle=null;
    let curr_toggle_word = null;
    let on_toggle_func = null;

    let words = {}

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
        addWord: (obj) => {
            words[obj.word] = obj
        },
        removeWord: (obj) => {
            if(words[obj.word]) delete words[obj.word]
        },
        getWord: (str) => { return(words[str]) },
        registerToggledObj: (elm) => {
            toggled_elm = elm;
            toggled_elm.style.display = is_toggle ? 'block' : 'none';
        },
        registerOnToggleFunc: (func) => {
            on_toggle_func = func;
        },
        isToggleOpen: () => {
            return is_toggle;
        },
        currToggleWord: () => {
            return curr_toggle_word;
        },
        changeToggle: (str, force_toggle = null) => {
            is_toggle = force_toggle == null ? !is_toggle : force_toggle;

            if(on_toggle_func && str) {
                on_toggle_func(str)
                curr_toggle_word = str
            }

            if(toggled_elm) toggled_elm.style.display = is_toggle ? 'block' : 'none';
        }
    };
})();

window.GameState = GameState;