from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, "Error, username already exists, Use another.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'register.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error, username already exists, Use another.")
            return redirect('login')
    return render(request, 'login.html', {})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def home(request):
    tasks = Task.objects.filter(user=request.user.id)
    return render(request, 'todo.html', {'tasks': tasks})

def add_task(request):
    if request.method == "POST":
        task_title = request.POST.get('task')
        if task_title:
            Task.objects.create(user=request.user, title=task_title)
    return redirect('home')

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('home')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')