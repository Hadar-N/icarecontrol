const INSTRUCTIONS_BY_STAGE = [
    {"recording": null, written_ref: ["dig_1", "dig_2"]},
    {"recording": null, written_ref: ["choose_and_match"]},
    {"recording": null, written_ref: ["wrong", "choose_again"]},
    {"recording": null, written_ref: ["success", "cover"]},
    {"recording": null, written_ref: ["cover"]}
]

class InstructionsLine {
    #container; #instruction_stage; #instructions_elm; #strings;

    constructor(container) {
        this.#container = container;
        this.#strings = GameState.getStrings()["gameprocess.html"].instructions;

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
        let rec = INSTRUCTIONS_BY_STAGE[this.#instruction_stage].recording;
        if (rec) {
            rec.play();
        }
    }

    getInstruction_stage() {
        return this.#instruction_stage;
    }

    applyInsructions(num) {
        this.#instruction_stage = num;
        console.log(this.#instruction_stage, this.#instructions_elm, this.#getFieldStr())
        this.#instructions_elm.innerHTML = this.#getFieldStr();
        this.#playRecording();
    }

}