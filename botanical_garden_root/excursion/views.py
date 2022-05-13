from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
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