from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from botanical_garden.decorators import allowed_users
# Create your views here.

@login_required(login_url='login')
@allowed_users(['customer'])
def excursion(request):
    context = {}
    return render(request, 'excursion/excursion.html', context)