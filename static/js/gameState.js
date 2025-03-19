const handleConsts = async () => {
    const constsNames = ["MQTT_DATA_ACTIONS", "GAME_STATUS"];

    let consts = {};
    let temp;
    for (c_name of constsNames) {
        temp = sessionStorage.getItem(c_name)
        if (temp) consts[c_name] = JSON.parse(temp)
    }

    if(!consts || !Object.keys(consts).length) {
        const res = await fetch('/getconstants', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        consts = await res.json()
        Object.entries(consts).forEach(([k,v]) => sessionStorage.setItem(k, JSON.stringify(v)))
    }
    return consts;
}

const GameState = (function () {
    let consts = {};
    handleConsts().then(res => consts = res)

    let toggled_elm= null;
    let is_toggle=null;
    let curr_toggle_word = null;
    let on_toggle_func = null;

    let words = {}

    return {
        getConsts: () => {
            if (!consts) {
                throw new Error("Consts not yet fetched!")
            }
            else return consts
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