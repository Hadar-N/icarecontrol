class SpeechManager {
    static #instance = null;
    
    static getInstance() {
        if (!SpeechManager.#instance) {
            SpeechManager.#instance = new SpeechManager();
        }
        return SpeechManager.#instance;
    }

    constructor() {
        if (SpeechManager.#instance) {
            throw new Error("SpeechManager is a singleton. Use SpeechManager.getInstance() instead.");
        }
        
        this.synth = window.speechSynthesis;
        this.currentUtterance = null;
        this.queue = [];
        this.speaking = false;
    }
    
    speak(text) {
        this.queue.push(text);
        if (!this.speaking) {
            this.processQueue();
        }
    }

    processQueue() {
        if (this.queue.length === 0) {
            this.speaking = false;
            this.cleanup();
            return;
        }

        this.speaking = true;
        const str = this.queue.shift();
        
        this.cleanup();
        this.createUtterance(str)

        this.synth.speak(this.currentUtterance);
    }

    createUtterance(str) {
        this.currentUtterance = new SpeechSynthesisUtterance(str);
        
        this.currentUtterance.onend = () => {
            this.cleanup();
            this.processQueue();
        };

        this.currentUtterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            this.cleanup();
            this.processQueue();
        };
    }

    cleanup() {
        if (this.currentUtterance) {
            this.currentUtterance.onend = null;
            this.currentUtterance.onerror = null;
            this.currentUtterance = null;
        }
    }

    clearQueue() {
        this.queue = [];
        this.synth.cancel();
        this.cleanup();
        this.speaking = false;
    }
}