from django.shortcuts import render,redirect
import requests
from django.http import JsonResponse
from .models import User, Asset
from .forms import UserForm,AssetForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login


def home(request): 
    return render(request, 'core/home.html')

from django.shortcuts import render
from django.http import JsonResponse
import requests

def assets(request):
    data = None

    if 'query' in request.GET:
        query = request.GET['query']
        try:
            api_url = f'https://brapi.dev/api/quote/list?&token=8rDXEbmSajqBqWekoG1rTh&search={query}'
            response = requests.get(api_url)
            data = response.json()
        except requests.RequestException as e:
            print(f"API request error: {e}")

    return render(request, 'core/assets.html', {'data': data})

def get_suggestions(request):
    data = None
    try:
        if 'query' in request.GET:
            query = request.GET['query']
            api_url = f'https://brapi.dev/api/quote/list?&token=8rDXEbmSajqBqWekoG1rTh'
            response = requests.get(api_url)
            data = response.json() 
            
            if data and 'stocks' in data:
                filtered_stocks = [stock for stock in data['stocks'] if query.lower() in stock['name'].lower()]
                data['stocks'] = filtered_stocks
    except requests.RequestException as e:
        print(f"API request error: {e}") 

    return JsonResponse({'data': data})

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('user_login')
    else:
        form = UserForm()
    return render(request, 'core/signup.html', {'form': form})

def show_users(request):
    users = User.objects.all()
    user_data = [{'id_user': user.id_user, 'name': user.name, 'age': user.age, 'cpf': user.cpf, 'email': user.email} for user in users]
    return JsonResponse({'users': user_data})

def create_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def show_assets(request):
    assets = Asset.objects.all()
    asset_data = [{'id_asset': asset.id_asset, 'name': asset.name, 'price': asset.price, 'price_tunel': asset.price_tunel, 'period': asset.period} for asset in assets]
    return JsonResponse({'assets': asset_data})

def user_assets_list(request, user_id):
    user = User.object.get(id_user= user_id)
    user_assets = user.assets.all()
    return render(request, 'user_assets.html', {'user_assets': user_assets})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid(): 
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
          

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Login inválido. Tente novamente.')

        print("form não é valido")
    else:
        form = LoginForm()
        

    return render(request, 'core/login.html', {'form': form})
