document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('form');
    var senhaInput = document.getElementById('senha');
    var confirmarSenhaInput = document.getElementById('confirmar_senha');
    var button = document.querySelector('button[type="submit"]');
    var cpfInput = document.getElementById('cpf');
    var telefoneInput = document.getElementById('telefone');

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

        return Object.values(requisitos).every(valor => valor === true);
    }

    function validarConfirmacaoSenha() {
        var senha = senhaInput.value;
        var confirmarSenha = confirmarSenhaInput.value;
        var mensagem = document.getElementById('mensagemConfirmacaoSenha');

        if (senha !== confirmarSenha) {
            mensagem.innerText = 'As senhas não coincidem.';
            return false;
        } else {
            mensagem.innerText = '';
            return true;
        }
    }

    function formatarCPF(campo) {
        var cpf = campo.value.replace(/\D/g, '');
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
        var telefone = campo.value.replace(/\D/g, '');
        if (telefone.length === 11) {
            telefone = '(' + telefone.substring(0, 2) + ') ' + telefone.substring(2, 7) + '-' + telefone.substring(7);
        } else {
            telefone = telefone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        }
        campo.value = telefone;
    }

    function verificarCampos() {
        var senhaValida = validarSenha(senhaInput);
        var confirmacaoValida = validarConfirmacaoSenha();
        var camposValidos = senhaValida && confirmacaoValida;

        button.disabled = !camposValidos;
    }

    senhaInput.addEventListener('input', verificarCampos);
    confirmarSenhaInput.addEventListener('input', verificarCampos);

    cpfInput.addEventListener('input', function() {
        formatarCPF(cpfInput);
    });

    telefoneInput.addEventListener('input', function() {
        formatarTelefone(telefoneInput);
    });

    form.addEventListener('submit', function (event) {
        if (!validarSenha(senhaInput) || !validarConfirmacaoSenha()) {
            event.preventDefault();
        }
    });

    verificarCampos();
});
