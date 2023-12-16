from django.shortcuts import render
import requests

def home(request):
    api_html = api_b3(request).content.decode('utf-8')
    return render(request, 'core/home.html', {'api_html': api_html})

def login(request):
    return render(request, 'core/login.html')

def api_b3(request):
    try:
        response = requests.get('https://brapi.dev/api/quote/PETR4?interval=1d&token=8rDXEbmSajqBqWekoG1rTh')
        data = response.json()
    except requests.RequestException as e:
        print(f"API request error: {e}")
        data = None
    return render(request, 'core/api.html', {'data': data})

