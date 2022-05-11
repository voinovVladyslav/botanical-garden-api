from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import Customer

from .forms import RegisterUserForm, CustomerForm
from botanical_garden.decorators import allowed_users, already_authenticated

# Create your views here.
@login_required(login_url='login')
@allowed_users(['customer'])
def profile(request):
    customer = request.user.customer
    
    context = {'customer':customer}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('profile')

    context = {'form':form, 'customer':customer}
    return render(request, 'accounts/settings.html', context)


@already_authenticated
def registerPage(request):

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(user=user, email=email)
            return redirect('login')

    else:
        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@already_authenticated
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('main')