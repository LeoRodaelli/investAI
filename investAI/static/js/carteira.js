const iconeMais = document.getElementById('icone-mais');

iconeMais.addEventListener('click', function() {
    const conteudo = document.querySelector('.conteudo');
    const novoFormulario = document.querySelector('.cadastroAcao').cloneNode(true);

    const iconeExcluir = document.createElement('div');
    iconeExcluir.classList.add('excluir');
    iconeExcluir.textContent = 'Excluir';
    iconeExcluir.style.width = '40px'; // Defina a largura desejada para o "x"
    iconeExcluir.style.cursor = 'pointer'; // Transforma o cursor em uma mãozinha ao passar por cima
    iconeExcluir.style.float = 'right'; // Alinha o "x" à direita

    iconeExcluir.addEventListener('click', function() {
        novoFormulario.remove();
    });

    novoFormulario.appendChild(iconeExcluir);
    conteudo.insertBefore(novoFormulario, iconeMais);
});

document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.querySelector('.cadastroAcao');
    const inputs = formulario.querySelectorAll('input, select');
    const button = document.querySelector('.button');

    function verificarCamposPreenchidos() {
        let todosPreenchidos = true;

        inputs.forEach(function(input) {
            if (!input.value.trim()) {
                todosPreenchidos = false;
            }
        });

        button.disabled = !todosPreenchidos;
    }

    inputs.forEach(function(input) {
        input.addEventListener('input', verificarCamposPreenchidos);
    });

    verificarCamposPreenchidos(); // Verifica os campos preenchidos ao carregar a página
});