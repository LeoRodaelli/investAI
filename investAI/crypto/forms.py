from django import forms
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Nome', 'id': 'name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email', 'id': 'email'}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "data"}), label='')
    telefone = forms.CharField(max_length=15, label='', widget=forms.TextInput(attrs={'placeholder': 'Telefone', 'id': 'telefone'}))
    cpf = forms.CharField(max_length=14, label='', widget=forms.TextInput(attrs={'placeholder': 'CPF', 'id': 'cpf'}))
    perfil_investidor = forms.ChoiceField(label='Tipo de Investidor', choices=[
        ('conservador', 'Conservador'),
        ('moderado', 'Moderado'),
        ('arrojado', 'Arrojado'),
    ], widget=forms.Select(attrs={'id':'perfil_investidor'}))
    senha = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'id': 'senha'}))
    confirmar_senha = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Senha', 'id': 'confirmar_senha'}))

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')

        if len(senha) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')

        if not re.search(r'[A-Z]', senha):
            raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')

        if not re.search(r'[0-9]', senha):
            raise ValidationError('A senha deve conter pelo menos um número.')

        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?]', senha):
            raise ValidationError('A senha deve conter pelo menos um caractere especial.')

        return senha

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Remover caracteres não numéricos do CPF
        cpf = ''.join(filter(str.isdigit, cpf))
        # Formatar CPF (###.###.###-##)
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        raise ValidationError('CPF inválido.')

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        # Remover caracteres não numéricos do telefone
        telefone = ''.join(filter(str.isdigit, telefone))
        # Formatar telefone
        if len(telefone) == 11:
            return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'
        raise ValidationError('Telefone inválido.')

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")


class LoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email', 'id': 'email'}))
    senha = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'id': 'senha'}))


class ProfileForm(forms.Form):
    perfil_investidor = forms.ChoiceField(label='', choices=[
        ('conservador', 'Conservador'),
        ('moderado', 'Moderado'),
        ('arrojado', 'Arrojado'),
    ], widget=forms.Select(attrs={'id':'perfil_investidor'}))


class WalletForm(forms.Form):
    acao_adquirida = forms.CharField(max_length=100, label='Ação adquirida:',widget=forms.TextInput(attrs={'placeholder': 'Ações', 'id': 'acao'}))
    categoria_acao = forms.ChoiceField(label='Categoria:', choices=[
        ('conservador', 'Conservador'),
        ('moderado', 'Moderado'),
        ('arrojado', 'Arrojado'),
    ], widget=forms.Select(attrs={'id':'categoria_acao'}))
