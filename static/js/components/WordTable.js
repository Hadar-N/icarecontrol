const MAX_OPTIONS = 3
const XV_INDICATORS = [
    {
        "class": "attempted",
        "sound": new Audio('/static/audio/fail.mp3'),
        "icon_url": "x.svg"
    }, {
        "class": "successful",
        "sound": new Audio('/static/audio/success.mp3'),
        "icon_url": "v.svg"
    }
]

// isEnglishMode(), createSpeakerButton, speakWord: defined in gameHelpers
// GameState and gameHelpers both imported in base.html

class WordTable {
    #container; #current_word; #current_chosen; #table_elm; #word_elm; #options_elm;

    constructor(container) {
        this.#container = container;
        this.#current_word = null;
        this.#current_chosen = null;

        this.#render()
        this.#initElm()
        this.#changeCurrChosen(null)
    }

    #htmlTemplate() {
        return `<table id="word-table">
            <tr>
                <th id="word-orig" class="word-orig">
                    <span id="for-speaker"></span>
                    <span id="word-txt"></span>
                </th>
            </tr>
            ${ Array.from({length: MAX_OPTIONS}, (e, i)=> i).map(ix => `
            <tr>
                <td id="opt-${ix}" class='option${ ix==(MAX_OPTIONS - 1) ? " last-item" : "" }' onclick="onOptionClick(this)">
                    <span id="for-speaker"></span>
                    <span id="opt_txt-${ix}" class="option-txt"></span>
                    <span id="for-result-img"></span>
                </td>
            </tr>
            `).join("")
            }
        </table>`
    }

    #render() {
        this.#container.innerHTML = this.#htmlTemplate()
    }

    #initElm() {
        this.#table_elm = document.getElementById('word-table');
        this.#word_elm = document.getElementById('word-orig');
        this.#options_elm = Array.from(document.getElementsByClassName('option'))
                            .sort((a, b) => Number(a.id.split('-')[1]) > Number(b.id.split('-')[1]) ? 1 : -1);
        this.#initSpeakers()
    }

    #initSpeakers() {
        let speaker_btn;
        if (isEnglishMode()) {
            speaker_btn = createSpeakerButton("speaker", false)
            speaker_btn.onclick = () => {
                if(this.#current_word) {
                    GameState.playClickAudio();
                    speakWord(this.#current_word.word);
            }}
            this.#word_elm.children[0].append(speaker_btn)
        } else {
            for (let i = 0; i < this.#options_elm.length; i++) {
                speaker_btn = createSpeakerButton("speaker", false)
                speaker_btn.onclick = () => {
                    if (this.#current_word && this.#current_word.options.length && !this.#current_word.options[i].is_attempted) {
                        GameState.playClickAudio();
                        speakWord(this.#current_word.options[i].word);
                    }
                }
                this.#options_elm[i].children[0].append(speaker_btn)
            }
        }
    }

    #changeCurrChosen = (new_chosen) => {
        if (this.#current_chosen) this.#options_elm[this.#current_chosen].classList.remove("active")
        if (Number.isInteger(new_chosen)) this.#options_elm[new_chosen].classList.add("active")
        this.#current_chosen = new_chosen
    }

    #createXVIcon = (url) => {
        let x_elm = document.createElement('img');
        x_elm.src = '/static/icons/' + url;
        x_elm.alt = url.split('.')[0]
        x_elm.classList.add("mini-img")
        return x_elm
    }

    isOptionsDisplayable = () => {
        return this.#current_word && !Number(this.#options_elm[0].style.opacity)
    }

    displayTable = (newword) => {
        this.#current_word = newword;
        if(isEnglishMode()) speakWord(this.#current_word.word);
        this.#word_elm.children[1].textContent = newword.word;
        this.#table_elm.style.opacity = 1
    }

    displayOptions = () => {
        this.#changeCurrChosen(null);
        let specific_opt, visual;
        for (let i = 0; i < this.#options_elm.length; i++) {
            specific_opt = this.#current_word.options[i]
            if (specific_opt.is_attempted && !this.#options_elm[i].children[2].children.length) {
                visual = XV_INDICATORS[Number(specific_opt.word == this.#current_word.meaning)];
                this.#options_elm[i].classList.add(visual.class);
                this.#options_elm[i].children[2].append(this.#createXVIcon(visual.icon_url));
                visual.sound.play();
            }
            this.#options_elm[i].children[1].textContent = specific_opt.word;
            this.#options_elm[i].style.opacity = 1;
        }
    }

    rerenderOptions = (newword) => {
        this.#changeCurrChosen(null)
        this.#current_word.options = newword.options;
        this.displayOptions();
    }

    matchedWord = () => {
        this.#changeCurrChosen()
        this.#current_word.options.find(o => o.word == this.#current_word.meaning).is_attempted = true;
        this.displayOptions();
    }

    onOptionClick = (e) => {
        new_id = e.id.split("-")[1];
        if (!this.#current_word.options[new_id].is_attempted) {
            GameState.playClickAudio();
            this.#changeCurrChosen(new_id)
            this.selectOptions(this.#current_word.word, this.#current_word.options[this.#current_chosen].word)
        }
    }

    turnoffTable = () => {
        this.#current_word = null;
        this.#changeCurrChosen(null)
        let xv_children;
        this.#options_elm.forEach(elm => {
            elm.style.opacity = 0;
            elm.classList.remove(...XV_INDICATORS.map(i => i.class))
            xv_children = elm.children[2].children
            for (let child of xv_children) elm.children[2].removeChild(child)
        })
        this.#table_elm.style.opacity = 0;
    }
}