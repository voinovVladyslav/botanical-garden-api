from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ContactForm


def thanks(request):
    return render(request, 'contact/thanks.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/thanks')

    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})