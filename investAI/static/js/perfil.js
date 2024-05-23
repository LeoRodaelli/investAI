const pergunta1 = document.getElementById('pergunta1');
const pergunta2 = document.getElementById('pergunta2');
const submitButton = document.getElementById('submitButton');

function checkInputs() {
    if (pergunta1.value !== "" && pergunta2.value !== "") {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

pergunta1.addEventListener('change', checkInputs);
pergunta2.addEventListener('change', checkInputs);
