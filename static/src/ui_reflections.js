function createTextElement(text, type="label") {
    let label = document.createElement(type);
    label.setAttribute("for", text)
    let description = document.createTextNode(text);
    label.appendChild(description);
    
    return label
}

// How the form to apply a new entry will look like
const type_gui_reflections = {
    "TextArea": (name, params, form) => {
        let textInput = document.createElement("textarea");
        textInput.setAttribute("name", name)
        textInput.rows = params["rows"];

        let div = document.createElement("div");
        div.appendChild(textInput);

        return {"input": div};
    },
    "Radio": (name, params, form) => {
        let fieldset = document.createElement("fieldset");
        fieldset.setAttribute("id", name);  
        fieldset.setAttribute("class", "form-check");
        params.values.forEach(value => {
            let div = document.createElement("div");
            let label = createTextElement(value)
            label.setAttribute("class", "form-check-label")
            let radio = document.createElement("input");
            radio.setAttribute("name", name)
            radio.setAttribute("value", value)
            radio.setAttribute("class", "form-check-input")
            radio.type = "radio";
            div.appendChild(label);
            div.appendChild(radio);
            fieldset.appendChild(div);
        });

        return {"input": fieldset};
    },
    "Checkbox": (name, params, form) => {
        let fieldset = document.createElement("fieldset");
        fieldset.setAttribute("id", name);   
        fieldset.setAttribute("class", "form-check");
        params.values.forEach(value => {
            let div = document.createElement("div");
            let label = createTextElement(value)
            label.setAttribute("class", "form-check-label")
            let checkbox = document.createElement("input");
            checkbox.setAttribute("name", name)
            checkbox.setAttribute("value", value)
            checkbox.setAttribute("class", "form-check-input")
            checkbox.type = "checkbox";
            div.appendChild(label);
            div.appendChild(checkbox);
            fieldset.appendChild(div);
        });

        return {"input": fieldset};
    }
}