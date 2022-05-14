from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from botanical_garden.decorators import allowed_users
from .models import Excursion
from datetime import date, datetime, timedelta
# Create your views here.


@login_required(login_url='login')
def excursions(request):
    excursions = request.user.customer.excursion_set.all()
    
    for excursion in excursions:
        excursion.excursion_time = excursion.excursion_time.strftime('%H:%M')
        excursion.excursion_date = excursion.excursion_date.strftime('%D')

    context = {'excursions':excursions}
    return render(request, 'excursion/excursions.html', context)


@login_required(login_url='login')
def excursions_delete(request, excursions_pk):
    excursion = request.user.customer.excursion_set.get(id=excursions_pk)

    if request.method == 'POST':
        excursion.delete()
        return redirect('excursions')

    context = {'excursion': excursion}
    return render(request, 'excursion/excursion_delete.html', context)


@allowed_users(['manager', 'admin'])
def excursions_all(request):
    excursions = Excursion.objects.all().order_by('excursion_date', 'excursion_time')
    today = date.today()
    upcoming = []
    passed = []

    for e in excursions:
        if e.excursion_date < today:
            e.excursion_time = e.excursion_time.strftime('%H:%M')
            e.excursion_date = e.excursion_date.strftime('%D')
            passed.append(e)
        else:
            e.excursion_time = e.excursion_time.strftime('%H:%M')
            e.excursion_date = e.excursion_date.strftime('%D')
            upcoming.append(e)
            

    context = {'upcoming': upcoming, 'passed': passed}
    return render(request, 'excursion/excursions_all.html', context)