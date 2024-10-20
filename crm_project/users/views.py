from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ManagerAccessForm, UserRegisterForm, UserUpdateForm
from .models import User, Profile

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)  
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile') 
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  


@login_required
def profile_view(request):
    profile = request.user.profile 
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def user_list_view(request):

    all_users = User.objects.all()

    managers = all_users.filter(is_manager=True)
    regular_users = all_users.filter(is_manager=False)

    return render(request, 'users/user_list.html', {
        'managers': managers,
        'regular_users': regular_users,
    })


def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)  
    return render(request, 'users/user_detail.html', {'user': user})    

@login_required
def edit_user_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'users/edit_user.html', {'form': form, 'user': user})


@login_required
def manage_access_view(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Проверка на роль пользователя: администратор или менеджер
    if request.user.is_admin:
        if request.method == 'POST':
            form = ManagerAccessForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('user-detail', pk=user.pk)  # перенаправление на страницу деталей пользователя
        else:
            form = ManagerAccessForm(instance=user)
        
        # Возвращаем форму для управления доступом
        return render(request, 'users/manage_access.html', {'form': form, 'user': user})

    # Если у пользователя нет прав, перенаправляем на список пользователей
    return redirect('user-list')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import User

@login_required
def user_list_view(request):
    query = request.GET.get('q', '')  
    role_filter = request.GET.get('role', '')  

    users = User.objects.all()

    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))

    if role_filter:
        if role_filter == 'manager':
            users = users.filter(is_manager=True)
        elif role_filter == 'regular':
            users = users.filter(is_manager=False)

    return render(request, 'users/user_list.html', {
        'users': users,
        'query': query,
        'role_filter': role_filter,  
    })
