document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form');
    var button = document.querySelector('button[type="submit"]');

    function verificarCampos() {
        var inputs = form.querySelectorAll('input');
        var camposPreenchidos = true;

        inputs.forEach(function(input) {
            if (input.value.trim() === '') {
                camposPreenchidos = false;
            }
        });

        button.disabled = !camposPreenchidos;
    }

    form.addEventListener('input', verificarCampos);
});


/* --------------------------- Adicionando a nav --------------------------------- */


