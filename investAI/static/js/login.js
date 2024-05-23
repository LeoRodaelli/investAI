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

/* Abrir tendencias */
document.addEventListener("DOMContentLoaded", function() {
    var modelButton = document.querySelector(".model");
    var popup = document.getElementById("popup");
    var closeButton = document.querySelector(".close");
    var selectElement = document.getElementById("listaAcoes");
    var tendenciaDiv = document.getElementById("tendencia");

    // Exibir o pop-up quando o botão "Veja as tendências aqui" for clicado
    modelButton.onclick = function() {
        popup.style.display = "block";
    }

    // Fechar o pop-up quando o botão de fechar for clicado
    closeButton.onclick = function() {
        popup.style.display = "none";
    }

    // Fechar o pop-up quando clicar fora dele
    window.onclick = function(event) {
        if (event.target == popup) {
            popup.style.display = "none";
        }
    }

    // Exibir a div "tendencia" quando uma opção for selecionada
    selectElement.addEventListener("change", function() {
        if (selectElement.value) {
            tendenciaDiv.style.display = "block";
        }
    });
});
