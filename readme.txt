step 1: python -m pip install --upgrade pip 
step 2: pip install pipenv
step 3: pipenv shell
step 4: pip install django 
step 5: python -m django startproject todo
step 6: cd todo
step 7: python manage.py startapp todoapp
step 8: python manage.py migrate
step 9: python manage.py runserver
step 10: Go to settings.py and add 'todoapp' this command in INSTALLED_APPS
step 11: Go to settings.py and add 'DIRS': ['templates'], this command in TEMPLATES
step 12: Go to urls.py in todo folder and the add this 

(from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todoapp.urls')),
])

step 13: create new file urls.py in todoapp and code as from (django.urls import path) and create urlpatterns = [] in it.
step 14: upload you html code in templates
step 15: After upload front-end then create code in views.py like this

def home(request):
    return render(request, 'todoapp/todo.html', {})

def register(request):
    return render(request, 'todoapp/register.html', {})

def login(request):
    return render(request, 'todoapp/login.html', {})

step 16: Then code 

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]

step 17: then code like in urls.py

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
    return render(request, 'todoapp/register.html', {})

step 18: code this in views.py

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
    return render(request, 'todoapp/login.html', {})

step 19: add this in both register.html and login.html

{% if messages %}
            {% for message in messages %}
                <div style="color: firebrick;">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <form action="#" method="POST">
            {% csrf_token %}
        </form>

step 20: add required name is all form fields username, email, password in both login.html and register.html
step 21: pip manage.py makemigrations
step 22: pip manage.py migrate
step 23: pip manage.py createsuperuser and create admin and login in the page to use.
step 24: pip manage.py runserver
step 25: manage.py to create code as 

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # link task to a user
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

step 26: add this code in views.py

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

step 27: add this code in urls.py

path('add/', views.add_task, name='add_task'),
path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
path('logout/', views.logout_view, name='logout'),

step 28: check in localhost /admin to see the users and superuser of application
step 29: pip manage.py migrate
step 30: pip manage.py runserver