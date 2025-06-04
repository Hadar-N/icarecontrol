class InstructionsLine {
    #container; #instruction_stage; #instructions_elm; #audio_elms; #strings; #flow_stage_to_instruction;
    
    constructor(container) {
        this.#container = container;
        this.#strings = GameState.getStrings()["gameprocess.html"].instructions;
        let flow_stages = GameState.getConsts().FLOW_STAGES
        this.#flow_stage_to_instruction = {
            [flow_stages.INITIAL]: ["dig_1"],
            [flow_stages.NEW_EN_WORD]: ["dig_2"],
            [flow_stages.BOTH_CONTOURS_READY]: ["choose_and_match"],
            [flow_stages.WRONG_MATCH]: ["wrong", "choose_again"],
            [flow_stages.SUCCESSFUL_MATCH]: ["success", "cover"],
            [flow_stages.NEED_REFRESH]: ["cover"]
        }
        this.#audio_elms = Object.values(this.#flow_stage_to_instruction).map(i => {
            return i.map(j => `static/recordings/${j}.mp3`)
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
        return this.#strings.symbol + ' ' + this.#flow_stage_to_instruction[this.#instruction_stage].map(k => this.#strings[k]).join('<br/>');
    }

    #playRecording() {
        this.#audio_elms[this.#instruction_stage].forEach(i => speakWord(i))
    }

    getInstruction_stage() {
        return this.#instruction_stage;
    }

    applyInsructions(stage) {
        if (stage !== this.#instruction_stage && this.#flow_stage_to_instruction[stage]) {
            this.#instruction_stage = stage;
            this.#instructions_elm.innerHTML = this.#getFieldStr();
            this.#playRecording();
        }
    }

}