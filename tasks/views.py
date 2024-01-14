from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'home.html')


# def signup(request):
#     if request.method == "GET":
#         return render(request, 'signup.html', {'form': UserCreationForm})
#     else:
#         username = request.POST['username']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         if password1 == password2:
#             try:

#                 user = User.objects.create(
#                     username=username, password=password1)
#                 user.save()
#                 login(request, user)
#                 # return HttpResponse("User created successfully")
#                 return redirect('tasks')
#             except IntegrityError as e:
#                 return render(request, 'signup.html', {
#                     'form': UserCreationForm(),
#                     'error': 'Username already exists'
#                 })

#         return render(request, 'signup.html', {
#             'form': UserCreationForm(),
#             'error': 'password do not match'
#         })


def signup(request):
    if request.method=='GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})
        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})
   
    # if request.method == "POST":
    #     form = RegistroUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password1']
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         messages.success(request, 'register finished')
    #         return redirect('home')
    

@login_required

def tasks(request):
    id_user = request.user.id

    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskForm, 'error': 'please provide valide data'})


# def signin(request):
#     if request.method == "GET":
#         return render(request, 'signin.html', {
#             'form': AuthenticationForm()
#         })
#     else:
#         print(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user=authenticate(request,username=username,password=password)
#         print(user)
#         if user is None:
#             return render(request, 'signin.html', {
#             'form': AuthenticationForm(),
#             'error':'Username or password is incorrect'
#         })
#         else:
#             login(request,user)
#             return redirect('tasks')

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')


@login_required
def task_detail(request, id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:

            task = get_object_or_404(Task, pk=id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "error updating in form"})


@login_required
def task_completed(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    print(task)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def tasks_completed(request):

    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')

    return render(request, 'tasks.html', {"tasks": tasks})
