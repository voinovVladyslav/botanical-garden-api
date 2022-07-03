from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from botanical_garden.decorators import allowed_users
from .models import Excursion
from .forms import ExcursionForm
from datetime import date 


def format_excursions(excursions):
    upcoming = []
    passed = []

    for e in excursions:
        if e.date < date.today():
            e.time = e.time.strftime('%H:%M')
            e.date = e.date.strftime('%D')
            passed.append(e)
        else:
            e.time = e.time.strftime('%H:%M')
            e.date = e.date.strftime('%D')
            upcoming.append(e)
    return upcoming, passed


@login_required(login_url='login')
def excursions(request):
    excursions = request.user.excursion_set.all().order_by('date', 'time')
    upcoming, passed = format_excursions(excursions)
    context = {'upcoming': upcoming, 'passed': passed}
    return render(request, 'excursion/excursions.html', context)


@login_required(login_url='login')
def excursions_delete_page(request, excursions_pk):
    excursion = request.user.excursion_set.get(id=excursions_pk)

    context = {'excursion': excursion}
    return render(request, 'excursion/excursion_delete.html', context)


@login_required(login_url='login')
def excursions_delete(request, excursions_pk):
    excursion = request.user.excursion_set.get(id=excursions_pk)

    if request.method == 'POST':
        excursion.delete()
        return redirect('excursions')
    raise Http404()


@allowed_users(['manager'])
def excursions_all(request):
    excursions = Excursion.objects.all().order_by('date', 'time')
    upcoming, passed = format_excursions(excursions)

    context = {'upcoming': upcoming, 'passed': passed}
    return render(request, 'excursion/excursions_all.html', context)
