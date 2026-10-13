import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

TMDB_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2N2RmM2NlYzVkMGI1NDRkMWM2MGIzMGExZjE1YTAyNSIsIm5iZiI6MTc5MTkxNzc3MC45MzYsInN1YiI6IjZhY2U3ZWNhZTUyMTliZmE3OWQ5NTY1ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fsN0J0v42p1LMzzJnwaVZmMi5mHqBoXhnyB_QrDfqns"

def fetch_and_save_shows(base_url, session_key, request):
    # Récupération de la page actuelle stockée en session (page 1 par défaut)
    current_page = request.session.get(session_key, 1)
    
    # Ajout du paramètre &page=X à l'URL TMDB
    url = f"{base_url}&page={current_page}"
    
    headers = {
        "Authorization": f"Bearer {TMDB_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        added_count = 0
        for show in results:
            # Exercice 4 : get_or_create évite les doublons via tmdb_id
            _, created = Task.objects.get_or_create(
                tmdb_id=show['id'],
                defaults={
                    'title': show['name'],
                    'complete': False
                }
            )
            if created:
                added_count += 1
            
            # S'arrête dès qu'on a ajouté 10 nouvelles séries valides
            if added_count >= 10:
                break

        # On incrémente la page en session pour le prochain clic
        request.session[session_key] = current_page + 1

def index(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)

def add_netflix(request):
    if request.method == 'POST':
        base_url = "https://api.themoviedb.org/3/discover/tv?with_networks=213&sort_by=vote_average.desc"
        fetch_and_save_shows(base_url, 'netflix_page', request)
    return redirect('/')

def add_amazon(request):
    if request.method == 'POST':
        base_url = "https://api.themoviedb.org/3/discover/tv?with_networks=1021&sort_by=vote_average.desc"
        fetch_and_save_shows(base_url, 'amazon_page', request)
    return redirect('/')

def add_appletv(request):
    if request.method == 'POST':
        base_url = "https://api.themoviedb.org/3/discover/tv?with_networks=2552&sort_by=vote_average.desc"
        fetch_and_save_shows(base_url, 'appletv_page', request)
    return redirect('/')

def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)

def deleteAllTasks(request):
    if request.method == 'POST':
        Task.objects.all().delete()
    return redirect('/')