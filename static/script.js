// Function to remove a variable input box
function removeVariable(event) {
    const variableInput = event.target.parentElement;
    variableInput.remove();
}

// Event listener for the "remove" button
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('remove-variable')) {
        removeVariable(event);
    }
});

// Function to add a new variable input box
function addVariable() {
    const variablesContainer = document.getElementById('variables-container');

    // Create the new variable input box
    const variableInput = document.createElement('div');
    variableInput.classList.add('variable-input');

    const variableNameInput = document.createElement('input');
    variableNameInput.setAttribute('type', 'text');
    variableNameInput.setAttribute('name', 'variable[]');
    variableNameInput.setAttribute('placeholder', 'variable');

    const valueInput = document.createElement('input');
    valueInput.setAttribute('type', 'text');
    valueInput.setAttribute('name', 'value[]');
    valueInput.setAttribute('placeholder', 'value');

    const removeButton = document.createElement('button');
    removeButton.setAttribute('type', 'button');
    removeButton.classList.add('remove-variable');
    removeButton.textContent = 'remove';

    // Add the elements to the variable input box
    variableInput.appendChild(variableNameInput);
    variableInput.appendChild(valueInput);
    variableInput.appendChild(removeButton);

    // Add the variable input box to the container
    variablesContainer.appendChild(variableInput);
}

// Event listener para o botão "Add Variable"
document.getElementById('add-variable').addEventListener('click', addVariable);
