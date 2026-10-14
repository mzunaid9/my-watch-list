import requests
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from .models import *
from .forms import *

logger = logging.getLogger(__name__)

TMDB_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2N2RmM2NlYzVkMGI1NDRkMWM2MGIzMGExZjE1YTAyNSIsIm5iZiI6MTc5MTkxNzc3MC45MzYsInN1YiI6IjZhY2U3ZWNhZTUyMTliZmE3OWQ5NTY1ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fsN0J0v42p1LMzzJnwaVZmMi5mHqBoXhnyB_QrDfqns"

def fetch_and_save_shows(endpoint_path, session_key, request):
    current_page = request.session.get(session_key, 1)
    
    base_url = getattr(settings, 'TMDB_API_BASE_URL', 'https://api.themoviedb.org/3')
    url = f"{base_url}/{endpoint_path}&page={current_page}"
    
    cache_key = f"tmdb_cache_{url}"
    data = cache.get(cache_key)
    
    if data is not None:
        # Log explicite pour le Cache HIT (Exercice 6)
        logger.info(f"[CACHE HIT] Données récupérées depuis Redis pour l'URL : {url}")
    else:
        # Log explicite pour le Cache MISS et l'appel sortant (Exercice 6)
        logger.info(f"[CACHE MISS] Appel sortant TMDB nécessaire pour l'URL : {url}")
        headers = {
            "Authorization": f"Bearer {TMDB_TOKEN}",
            "accept": "application/json"
        }
        try:
            response = requests.get(url, headers=headers, timeout=(3.0, 3.0))
            
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, timeout=300)
                logger.info("Appel API TMDB réussi et mis en cache Redis avec succès.")
            else:
                logger.error(f"Erreur API TMDB - Status code: {response.status_code}")
                messages.error(request, "Erreur lors de la récupération des données auprès de TMDB.")
                return False
        except requests.exceptions.Timeout:
            logger.warning("Timeout (avertissement) : Le service TMDB met trop de temps à répondre.")
            messages.error(request, "Le service TMDB met trop de temps à répondre. Réessayez plus tard.")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur critique - Impossible de joindre TMDB : {e}")
            messages.error(request, "Impossible de joindre le service TMDB pour le moment.")
            return False

    results = data.get('results', [])
    added_count = 0
    for show in results:
        exists = Task.objects.filter(user=request.user, tmdb_id=show['id']).exists()
        if not exists:
            Task.objects.create(
                user=request.user,
                tmdb_id=show['id'],
                title=show['name'],
                complete=False
            )
            added_count += 1
            
        if added_count >= 10:
            break

    request.session[session_key] = current_page + 1
    return True

@login_required(login_url='login')
def index(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user 
            task.save()
        return redirect('/')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)

@login_required(login_url='login')
def add_netflix(request):
    if request.method == 'POST':
        fetch_and_save_shows("discover/tv?with_networks=213&sort_by=vote_average.desc", 'netflix_page', request)
    return redirect('/')

@login_required(login_url='login')
def add_amazon(request):
    if request.method == 'POST':
        fetch_and_save_shows("discover/tv?with_networks=1021&sort_by=vote_average.desc", 'amazon_page', request)
    return redirect('/')

@login_required(login_url='login')
def add_appletv(request):
    if request.method == 'POST':
        fetch_and_save_shows("discover/tv?with_networks=2552&sort_by=vote_average.desc", 'appletv_page', request)
    return redirect('/')

@login_required(login_url='login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)

@login_required(login_url='login')
def deleteTask(request, pk):
    item = Task.objects.get(id=pk, user=request.user)

    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)

@login_required(login_url='login')
def deleteAllTasks(request):
    if request.method == 'POST':
        Task.objects.filter(user=request.user).delete()
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'tasks/register.html', context)