from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import MongoClient
from .forms import RegistrationForm, LoginForm, ProfileForm, WalletForm

connection_string = "mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest"
client = MongoClient(connection_string)

class Index(TemplateView):
    template_name = 'index.html'

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

            nome = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            data = form.cleaned_data["date"]
            celular = form.cleaned_data["telefone"]
            cpf = form.cleaned_data["cpf"]
            perfil = form.cleaned_data["perfil_investidor"]
            senha = form.cleaned_data["senha"]

            data = str(data)

            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")  # Insira a sua connection string aqui
            db = mongo_client["Invest"]
            collection = db["Usuarios"]

            document = {
                "nome": nome,
                "email": email,
                "celular": celular,
                "cpf": cpf,
                "senha": senha,
                "data": data,
                "perfil": perfil
            }

            collection.insert_one(document)

            print(f"Usuário adicionado com sucesso!")

        return redirect("home")
    else:
        form = RegistrationForm()
    return render(response, "register.html", {'form': form })

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")
            db = mongo_client["Invest"]
            user_collection = db["Usuarios"]
            prediction_collection = db["predictions"]

            usuario = user_collection.find_one({"email": email, "senha": senha})
            previsao = prediction_collection.find_one({"model": "GradientBoosting"})

            if usuario:

                usuario["_id"] = str(usuario["_id"])
                if previsao and "_id" in previsao:
                    previsao["_id"] = str(previsao["_id"])
                # Armazenando informações na sessão
                request.session['email'] = email
                request.session['usuarioName'] = usuario["nome"]
                request.session['cpf'] = usuario["cpf"]
                request.session['perfil'] = usuario["perfil"]
                request.session['previsao'] = previsao

                print(usuario['perfil'])

                return redirect('homeLogado')  # Nome da URL para a página de destino
            else:
                return redirect("login")
    else:
        form = LoginForm()

    return render(request, "login.html", {'form': form})

# views.py para a página homeLogado
def homeLogado(request):

    mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")
    db = mongo_client["Invest"]
    prediction_collection = db["predictions"]

    email = request.session.get('email')
    usuarioName = request.session.get('usuarioName')
    cpf = request.session.get('cpf')
    perfil = request.session.get('perfil')

    previsoes = []
    for prediction in prediction_collection.find():
        if prediction["model"] == "GradientBoosting":
            previsoes.append({
                'ticker': prediction['ticker'],
                'trend': prediction["trend"],
                'prediction': prediction["prediction"],
                'overall_trend': prediction["overall_trend"],
                'prediction_date': prediction["prediction_date"],
            })

    return render(request, "homeLogado.html", {
        'email': email, 
        'previsao': previsoes, 
        'usuarioName': usuarioName,
        'cpf': cpf,
        'perfil': perfil
    })


def perfil(request):

    perfil = request.session.get('perfil')
    email = request.session.get("email")
    senha = request.session.get("senha")

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            novoPerfil = form.cleaned_data["perfil_investidor"]

            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")
            db = mongo_client["Invest"]
            user_collection = db["Usuarios"]

            filtro = {"email": email}
            novoValor = { "$set": { "perfil": novoPerfil } }

            user_collection.update_one(filtro, novoValor)

            request.session['perfil'] = novoPerfil
        
        return redirect("homeLogado")

    else:
        form = ProfileForm()
    return render(request, "perfil.html", {
        'perfil': perfil, 'form': form
    })


def carteira(request):
    email = request.session.get('email')

    # Conectar ao MongoDB
    mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")
    db = mongo_client["Invest"]
    collection = db["Usuarios"]

    # Buscar a carteira do usuário no banco de dados
    usuario = collection.find_one({"email": email})
    acoes = usuario.get('acoes', [])

    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            acao_adquirida = form.cleaned_data["acao_adquirida"]
            categoria_acao = form.cleaned_data["categoria_acao"]

            # Adicionar a nova ação à carteira do usuário
            nova_acao = {"acao_adquirida": acao_adquirida, "categoria_acao": categoria_acao}
            collection.update_one({"email": email}, {"$push": {"acoes": nova_acao}})

            # Atualizar a lista de ações na sessão (opcional)
            request.session['acoes'] = acoes + [nova_acao]

            return redirect("homeLogado")
    else:
        form = WalletForm()

    return render(request, "carteira.html", {'form': form, 'acoes': acoes})

