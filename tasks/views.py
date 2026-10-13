import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *

TMDB_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2N2RmM2NlYzVkMGI1NDRkMWM2MGIzMGExZjE1YTAyNSIsIm5iZiI6MTc5MTkxNzc3MC45MzYsInN1YiI6IjZhY2U3ZWNhZTUyMTliZmE3OWQ5NTY1ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fsN0J0v42p1LMzzJnwaVZmMi5mHqBoXhnyB_QrDfqns"

def fetch_and_save_shows(base_url, session_key, request):
    current_page = request.session.get(session_key, 1)
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
            # On vérifie si l'utilisateur a déjà cette série dans sa propre watchlist
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

@login_required(login_url='login')
def index(request):
    # L'utilisateur ne voit que ses propres tâches (Exercice 5)
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # On associe la tâche à l'utilisateur connecté
            task.save()
        return redirect('/')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)

@login_required(login_url='login')
def add_netflix(request):
    if request.method == 'POST':
        base_url = "https://api.themoviedb.org/3/discover/tv?with_networks=213&sort_by=vote_average.desc"
        fetch_and_save_shows(base_url, 'netflix_page', request)
    return redirect('/')

@login_required(login_url='login')
def add_amazon(request):
    if request.method == 'POST':
        base_url = "https://api.themoviedb.org/3/discover/tv?with_networks=1021&sort_by=vote_average.desc"
        fetch_and_save_shows(base_url, 'amazon_page', request)
    return redirect('/')

@login_required(login_url='login')
def add_appletv(request):
    if request.method == 'POST':
        base_url = "https://api.themoviedb.org/3/discover/tv?with_networks=2552&sort_by=vote_average.desc"
        fetch_and_save_shows(base_url, 'appletv_page', request)
    return redirect('/')

@login_required(login_url='login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk, user=request.user) # Sécurité : appartient à l'utilisateur
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
    item = Task.objects.get(id=pk, user=request.user) # Sécurité

    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)

@login_required(login_url='login')
def deleteAllTasks(request):
    if request.method == 'POST':
        Task.objects.filter(user=request.user).delete() # Supprime uniquement les siennes
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