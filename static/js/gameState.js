// Create a module for shared state
const GameState = (function () {
    const constsNames = ["MQTT_DATA_ACTIONS", "GAME_STATUS"]
    let consts = {}
    let temp;
    for (c_name of constsNames) {
        temp = sessionStorage.getItem(c_name)
        if (temp) consts[c_name] = JSON.parse(temp)
    }

    if(!consts || !Object.keys(consts).length) {
        fetch('/getconstants', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(res => {
            Object.entries(res).forEach(([k,v]) => sessionStorage.setItem(k, JSON.stringify(v)))
            consts = res
        })
    }

    return {
        getConsts: function () {
            if (!consts) {
                throw new Error("Consts not yet fetched!")
            }
            else return consts
        }

    };
})();

window.GameState = GameState;