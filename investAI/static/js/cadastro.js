document.addEventListener('DOMContentLoaded', function () {
    var dataNascimento = document.getElementById('data');
    var mensagemIdade = document.getElementById('mensagemIdade');

    dataNascimento.addEventListener('change', function () {
        var hoje = new Date();
        var data = new Date(this.value);
        var idade = hoje.getFullYear() - data.getFullYear();

        if (hoje.getMonth() < data.getMonth() || (hoje.getMonth() == data.getMonth() && hoje.getDate() < data.getDate())) {
            idade--;
        }

        if (idade < 18) {
            mensagemIdade.innerText = 'É necessário ser maior de 18 anos.';
            this.setCustomValidity('É necessário ser maior de 18 anos.');
        } else {
            mensagemIdade.innerText = '';
            this.setCustomValidity('');
        }
    });
});



function formatarCPF(campo) {
    var cpf = campo.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    if (cpf.length > 3 && cpf.length <= 6) {
        cpf = cpf.substring(0, 3) + '.' + cpf.substring(3);
    } else if (cpf.length > 6 && cpf.length <= 9) {
        cpf = cpf.substring(0, 3) + '.' + cpf.substring(3, 6) + '.' + cpf.substring(6);
    } else if (cpf.length > 9 && cpf.length <= 11) {
        cpf = cpf.substring(0, 3) + '.' + cpf.substring(3, 6) + '.' + cpf.substring(6, 9) + '-' + cpf.substring(9);
    }
    campo.value = cpf;
}

function formatarTelefone(campo) {
    var telefone = campo.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    if (telefone.length === 11) {
        telefone = '(' + telefone.substring(0, 2) + ') ' + telefone.substring(2, 7) + '-' + telefone.substring(7);
    } else {
        telefone = telefone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    }
    campo.value = telefone;
}

function validarSenha(campo) {
    var senha = campo.value;
    var requisitos = {
        letraMaiuscula: /[A-Z]/.test(senha),
        numero: /[0-9]/.test(senha),
        especial: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/.test(senha),
        tamanho: senha.length >= 8
    };

    for (var requisito in requisitos) {
        var elemento = document.getElementById(requisito);
        if (requisitos[requisito]) {
            elemento.style.color = 'gray';
        } else {
            elemento.style.color = 'red';
        }
    }

    var mensagem = document.getElementById('mensagemSenha');
    if (Object.values(requisitos).every(valor => valor === true)) {
        mensagem.innerText = '';
    } else {
        mensagem.innerText = 'A senha não atende aos requisitos.';
    }
}



function validarConfirmacaoSenha() {
    var senha = document.getElementById('senha').value;
    var confirmarSenha = document.getElementById('confirmarSenha').value;
    var mensagem = document.getElementById('mensagemConfirmacaoSenha');

    if (senha !== confirmarSenha) {
        mensagem.innerText = 'As senhas não coincidem.';
    } else {
        mensagem.innerText = '';
    }
}


document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('form');
    var button = document.querySelector('button[type="submit"]');

    function verificarCampos() {
        var inputs = form.querySelectorAll('input');
        var camposValidos = true;

        inputs.forEach(function (input) {
            if (!input.checkValidity()) {
                camposValidos = false;
            }
        });

        button.disabled = !camposValidos;
    }

    form.addEventListener('input', verificarCampos);
});


document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('form');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Previne o comportamento padrão de envio do formulário

        // Aqui você pode adicionar o código para enviar os dados do formulário
    });
});


/* --------------------------- Adicionando a nav --------------------------------- */

window.addEventListener('DOMContentLoaded', function () {
    fetch('../../crypto/templates/nav.html')  // Caminho relativo para o arquivo nav.html
        .then(response => response.text())
        .then(html => {
            document.getElementById('nav').innerHTML = html;
        });
});
