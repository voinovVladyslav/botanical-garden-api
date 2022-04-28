from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegisterUserForm

# Create your views here.
def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)

def registerPage(request):   

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'account was created for' + user)

    else:
        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid data')

    context = {}
    return render(request, 'accounts/login.html', {})


def logoutUser(request):
    logout(request)
    return redirect('/auth/login')