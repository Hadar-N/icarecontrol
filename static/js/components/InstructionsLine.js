const INSTRUCTIONS_BY_STAGE = [
    { written_ref: ["dig_1", "dig_2"] },
    { written_ref: ["choose_and_match"] },
    { written_ref: ["wrong", "choose_again"] },
    { written_ref: ["success", "cover"] },
    { written_ref: ["cover"] }
]

class InstructionsLine {
    #container; #instruction_stage; #instructions_elm; #audio_elms; #strings;

    constructor(container) {
        this.#container = container;
        this.#strings = GameState.getStrings()["gameprocess.html"].instructions;
        this.#audio_elms = INSTRUCTIONS_BY_STAGE.map(i => {
            return i.written_ref.map(j => `static/recordings/${j}.mp3`)
        });

        this.#parentRender();
        this.#initElm();
        this.applyInsructions(0);
    }

    #parentRender() {
        this.#container.innerHTML = `<div id="instructions" class="instructions"></div>`;
    }

    #initElm() {
        this.#instructions_elm = document.getElementById('instructions');
    }

    #getFieldStr() {
        return this.#strings.symbol + ' ' + INSTRUCTIONS_BY_STAGE[this.#instruction_stage].written_ref.map(k => this.#strings[k]).join('<br/>');
    }

    #playRecording() {
        this.#audio_elms[this.#instruction_stage].forEach(i => speakWord(i))
    }

    getInstruction_stage() {
        return this.#instruction_stage;
    }

    applyInsructions(num) {
        if (num !== this.#instruction_stage) {
            this.#instruction_stage = num;
            this.#instructions_elm.innerHTML = this.#getFieldStr();
            this.#playRecording();
        }
    }

}