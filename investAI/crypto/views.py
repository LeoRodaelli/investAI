from django.views.generic import TemplateView
from django.shortcuts import render
from pymongo import MongoClient
from django.conf import settings
from django.shortcuts import redirect, reverse

connection_string = "mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest"
client = MongoClient(connection_string)

class Index(TemplateView):
    template_name = 'index.html'


class Register(TemplateView):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = self.request.POST.get('email')
        name = self.request.POST.get('name')
        telephone = self.request.POST.get('telefone')
        cpf = self.request.POST.get('cpf')
        password = self.request.POST.get('senhar')
        confirm_password = self.request.POST.get('confirmarSenha')
        print("Post")

        try:
            mongo_client = MongoClient(connection_string)
            db = client["Invest"]
            users_collection = db["Usuarios"]

            if users_collection.find_one({'email': email}):
                mongo_client.close()
                return render(request, self.template_name, {'error': 'E-mail já cadastrado', 'email': email})

            elif password != confirm_password:
                mongo_client.close()
                return render(request, self.template_name, {'error': 'As senhas são diferentes', 'email': email})

            else:
                users_collection.insert_one({'nome': name, 'email': email,'celular':telephone,'cpf': cpf, 'senha': password})
                mongo_client.close()

            login_url = reverse('crypto:login') + f'?email={email}'
            return redirect(login_url)
        except Exception as e:
            # Se ocorrer algum erro, imprima-o no terminal do servidor Django
            print("Erro ao inserir dados no MongoDB:", e)
            # Retorne uma resposta indicando que ocorreu um erro, por exemplo:
            return render(request, self.template_name, {'error': 'Ocorreu um erro ao processar seu registro.'})


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
            return redirect(reverse('crypto:Home'))

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


def nav(request):
    return render(request, 'nav.html')

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')


