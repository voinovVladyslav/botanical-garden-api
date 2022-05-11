from django.shortcuts import redirect, render

from excursion.forms import ExcursionForm


def main(request):
    
    if request.method == "POST":
        form = ExcursionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.person = request.user.customer
            t.save()
            return redirect('profile')
    else:
        form = ExcursionForm()

    context = {'form': form}
    return render(request, 'pages/main.html', context)


def history(request):
    return render(request, 'pages/history.html')


def structure(request):
    return render(request, 'pages/structure.html')
