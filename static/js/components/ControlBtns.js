class ControlBtns {
    #container; #btns;
    
    constructor(container) {
        this.#container = container;
        this.#btns = ['home', 'return']
        this.#initElm();
    }

    #renderSingleBtn(btn) {
        return `<input type="radio" name="ctrl-buttons" id="${btn}" value="${btn}" />
            <label for="${btn}" class="ctrl-singlebutton" id="${btn}">
                <img class="ctrl-img" src="/static/icons/${btn}.svg" alt="${btn}" />
            </label>`
    }
    
    #initElm() {
        this.#container.innerHTML = `<div class="ctrl-buttons">${this.#btns.map(btn => this.#renderSingleBtn(btn)).join('')}</div>`
        Array.from(document.getElementsByClassName('ctrl-singlebutton')).forEach(btn => btn.addEventListener('click', () => this.#onClickControl(btn)))
    }

    #onClickControl = (obj) => {
            GameState.playClickAudio();
            clickControlFunc("stop", {mode: obj.getAttribute("id") == "home" ? 0 : GameState.getCurrModeStr(true)});
        }


}