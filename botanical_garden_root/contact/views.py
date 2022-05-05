from django.shortcuts import render
from django.http import HttpResponseRedirect

from news.decorators import allowed_users
from .forms import ContactForm
from .models import Contact

def thanks(request):
    return render(request, 'contact/thanks.html')


def contact(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            return HttpResponseRedirect('thanks')

    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})


@allowed_users(['manager', 'admin'])
def contact_all(request):
    contacts = Contact.objects.all()

    context = {'contacts':contacts}
    return render(request, 'contact/contact_all.html', context)


@allowed_users(['manager', 'admin'])
def contact_single(request, contact_pk):
    contact = Contact.objects.get(id=contact_pk)

    context = {'contact':contact}
    return render(request, 'contact/contact_single.html', context)