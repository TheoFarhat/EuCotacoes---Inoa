from django.shortcuts import render
import requests
from django.http import JsonResponse

def home(request): 
    return render(request, 'core/home.html')

def login(request):
    return render(request, 'core/login.html')


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
