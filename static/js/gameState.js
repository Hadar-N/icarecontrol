function parseFromFlaskJson(str) {
    return JSON.parse(str.replaceAll(/(&#34;)|(&#39;)|(&lt;)|(&gt;)/g, '"').replaceAll("None", "null"));
}

const GameState = (function () {
    let consts = {};
    let strings = {};


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
        }
    };
})();

window.GameState = GameState;