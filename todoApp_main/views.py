from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template.defaultfilters import title

from .models import Task, SubTask, Projects
from .forms import TaskForm,ProjectsForm

from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm





def login_page(request):
    page = 'login'
    context = {'page':page}

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"user doesn't exists")

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exist')
    return render(request,'todoApp_main/login_page.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user) 
            return redirect('home')

    context = {'form':form}
    return render(request,'todoApp_main/login_page.html',context)

@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''


    projects = Projects.objects.filter(Q(name__icontains = q),admin = request.user)

    projects_amount = projects.count()


    context = {'projects':projects,'projects_amount':projects_amount}
    return render(request,'todoApp_main/home.html',context)


@login_required(login_url='login')
def project(request,pk):
    project = Projects.objects.get(id = pk)
    if request.user != project.admin and not project.users.filter(id=request.user.id).exists():
        return redirect('not_allowed')

    tasks = project.tasks.all()
    users = project.users.all()
    project_id = pk
    print(users)

    return render(request,'todoApp_main/project_page.html',{'tasks':tasks,'project_id':project_id,'users':users})

@login_required(login_url='login')
def project_create(request):
    form = ProjectsForm()

    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.admin = request.user
            project.save()
            form.save_m2m() # to save many to many users
            project.users.add(request.user)

        return redirect('home')


    context = {'form' : form}

    return render(request,'todoApp_main/project_create.html',context)


@login_required(login_url='login')
def not_allowed(request):
    return render(request,'todoApp_main/not_allowed.html',{})


@login_required(login_url='login')
def task(request,pk):
    task = Task.objects.get(id = pk)
    sub_tasks = SubTask.objects.filter(parent_task = pk)





    context = {'task': task, 'subtask' : sub_tasks}
    return render(request,'todoApp_main/task.html',context)

@login_required(login_url="login")
def create_task(request,pk):
    form = TaskForm()
    target_project = Projects.objects.get(id = pk)

    referer_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        task = Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            status=status,
            priority=priority,
            deadline=deadline,
        )

        target_project.tasks.add(task)




        return redirect('home')


    context = {'form' : form}
    return render(request,'todoApp_main/task_create.html',context)

@login_required(login_url='login')
def update_task(request, pk):
    task = Task.objects.get(id = pk)
    form =  TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {'form':form}

    return render(request,"todoApp_main/task_update.html",context)

@login_required(login_url='login')
def delete_task(request,pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request,"todoApp_main/task_delete.html",{'task':task})













