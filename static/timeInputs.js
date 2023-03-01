class timeInputs {
    constructor(start, end, inputs) {
        this.start_inputs = start;
        this.end_inputs = end;
        this.all_inputs = inputs;
    }

    toggleInputs(isActive){
        this.all_inputs.forEach(input => {
            input.disabled = !isActive;
        });

    }

    getTime() {
        return {
            start: Array.from(this.start_inputs).map(e => { return e.value; }),
            end: Array.from(this.end_inputs).map(e => { return e.value; })
        };
    }
}

export { timeInputs };