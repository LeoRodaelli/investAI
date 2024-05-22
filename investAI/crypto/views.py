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
            user_data = form.cleaned_data

            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")
            db = mongo_client["Invest"]
            collection = db["Usuarios"]

            collection.insert_one(user_data)
            print("Usuário adicionado com sucesso!")

            return redirect("home")
        else:
            print("Formulário de registro não é válido.")
    else:
        form = RegistrationForm()

    return render(response, "register.html", {'form': form})


def login(response):
    if response.method == "POST":
        form = LoginForm(response.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            mongo_client = MongoClient("mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest")  # Insira a sua connection string aqui
            db = mongo_client["Invest"]
            user_collection = db["Usuarios"]
            prediction_collection = db["predictions"]

            usuario = user_collection.find_one({"email": email, "senha": senha})
            previsao = prediction_collection.find()

            if usuario:
                for i in previsao:
                    print(i)
                return (HttpResponse(f"Usuário encontrado {usuario}"))
            else:
                return HttpResponse("Usuário não encontrado")
            
    else:
        form = LoginForm()

    return render(response, "login.html", {'form': form })
