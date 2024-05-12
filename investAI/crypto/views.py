from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import MongoClient
from .forms import RegistrationForm, LoginForm

connection_string = "mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest"
client = MongoClient(connection_string)

class Index(TemplateView):
    template_name = 'index.html'

class Register(TemplateView):
    template_name = 'register.html'

    def get(self, response):
        print("Tela de registro carregada")
        return render(response, self.template_name)

    def post(self, response):
        print("Tentando fazer o registro")

        try:
            # Receber dados do formulário
            email = response.POST.get('email')
            name = response.POST.get('name')
            telephone = response.POST.get('telefone')
            cpf = response.POST.get('cpf')
            password = response.POST.get('senha')
            confirm_password = response.POST.get('confirmarSenha')

            # Configurar conexão com o MongoDB
            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")  # Insira a sua connection string aqui
            db = mongo_client["Invest"]
            collection = db["Usuarios"]

            # Criar documento para inserção no MongoDB
            document = {
                "nome": name,
                "email": email,
                "celular": telephone,
                "cpf": cpf,
                "senha": password,
            }

            # Inserir documento na coleção
            collection.insert_one(document)

            print(f"Usuário '{name}' adicionado com sucesso!")

            # Redirecionar para a página inicial
            return render(response, 'home.html')
        
        except Exception as e:
            print(f"Erro ao processar o formulário: {e}")
            return render(response, self.template_name, {'error_message': 'Erro ao processar o formulário. Por favor, tente novamente.'})


class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        email = self.request.GET.get('email', '')

        return render(request, self.template_name, {'email': email})

    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        mongo_client = MongoClient(connection_string)
        db = mongo_client.Data
        users_collection = db.UsersAccounts
        user = users_collection.find_one({'email': email, 'password': password})

        if user:
            mongo_client.close()
            return render(request, 'home.html')

        mongo_client.close()
        return render(request, self.template_name, {'error': 'E-mail não cadastrado ou senha inválida', 'email': email})


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mongo_client = MongoClient(connection_string)
        db = mongo_client.Data
        ml_collection = db.MachineLearningData

        recommendations = []

        for mongo_set in ml_collection.find():
            symbol = mongo_set['symbol']
            price = mongo_set['price']
            recommendation = mongo_set['recommendation']
            moving_average = mongo_set['moving average']

            recommendations.append((symbol, price, recommendation, moving_average))

        context['recommendations'] = recommendations

        mongo_client.close()
        return context

class Nav(TemplateView):
    template_name = 'nav.html'

    def get(self, request):
        return render(request, self.template_name)

def register(response):
    if response.method == "POST":
        form = RegistrationForm(response.POST)

        if form.is_valid():

            nome = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            data = form.cleaned_data["date"]
            celular = form.cleaned_data["telefone"]
            cpf = form.cleaned_data["cpf"]
            senha = form.cleaned_data["senha"]
            confirmar_senha = form.cleaned_data["confirmar_senha"]

            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")  # Insira a sua connection string aqui
            db = mongo_client["Invest"]
            collection = db["Usuarios"]

            document = {
                "nome": nome,
                "email": email,
                "celular": celular,
                "cpf": cpf,
                "senha": senha,
            }

            collection.insert_one(document)

            print(f"Usuário adicionado com sucesso!")

        return redirect("home")
    else:
        form = RegistrationForm()
    return render(response, "register.html", {'form': form })


def login(response):
    if response.method == "POST":
        form = LoginForm(response.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")  # Insira a sua connection string aqui
            db = mongo_client["Invest"]
            collection = db["Usuarios"]

            usuario = collection.find_one({"email": email, "senha": senha})

            if usuario:
                return HttpResponse("Usuário encontrado")
            else:
                return HttpResponse("Usuário não encontrado")
            
    else:
        form = LoginForm()

    return render(response, "login.html", {'form': form })
