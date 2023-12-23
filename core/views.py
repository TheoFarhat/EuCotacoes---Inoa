from django.shortcuts import render,redirect, get_object_or_404
import requests
from django.http import JsonResponse
from .models import User, Asset
from .forms import UserForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os


@login_required
def home(request):
    user = request.user
    assets = user.assets.all()

    context = {'user': user, 'assets': assets, 'user_id': user.id_user}

    return render(request, 'core/home.html', context)

@login_required
def profile(request):
    user = request.user
   

    context = {'user': user}

    return render(request, 'core/profile.html', context)


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
    user_data = []
    for user in users:
        user_info = {
            'id_user': user.id_user,
            'name': user.name,
            'age': user.age,
            'cpf': user.cpf,
            'email': user.email,
            'assets': [{'id_asset': asset.id_asset, 'name': asset.name, 'price': asset.price,'image_url':asset.image.url if asset.image else None} for asset in user.assets.all()]
        }
        user_data.append(user_info)

    return JsonResponse({'users': user_data})


@login_required
@require_POST
def create_asset(request):
    user = request.user

    stock = request.POST.get('stock')
    period = request.POST.get('period')
    lower_tunnel_price = float(request.POST.get('lower_tunnel_price'))
    upper_tunnel_price = float(request.POST.get('upper_tunnel_price'))

    api_url = f'https://brapi.dev/api/quote/{stock}?interval={period}&token=8rDXEbmSajqBqWekoG1rTh'
    api_response = requests.get(api_url)
    api_data = api_response.json()
    print(api_data)

    asset_name = api_data['results'][0]['shortName']
    asset_symbol = api_data['results'][0]['symbol']
    asset_price = api_data['results'][0]['regularMarketPrice']
    asset_previous_close = api_data['results'][0]['regularMarketPreviousClose']

    image_url = api_data['results'][0]['logourl']
    image_filename = os.path.basename(urlparse(image_url).path)

    percentage_change = round((((asset_price - asset_previous_close) / asset_previous_close) * 100), 2)

    asset = Asset(
        name=asset_name,
        symbol = asset_symbol,
        price=asset_price,
        period=period,
        lower_tunnel_price = lower_tunnel_price,
        upper_tunnel_price = upper_tunnel_price,
        percentage_change = percentage_change
    )
    asset.save()

    asset.image.save(image_filename, ContentFile(requests.get(image_url).content), save=True)
    user.assets.add(asset)

    return redirect('home') 




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

@login_required
def remove_asset(request):
    if request.method == 'POST':
        asset_id = request.POST.get('asset_id')
        csrf_token = request.POST.get('csrfmiddlewaretoken')

    
        asset = get_object_or_404(Asset, id_asset=asset_id)

        asset.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})