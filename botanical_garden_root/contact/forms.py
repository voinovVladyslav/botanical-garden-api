from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше ім'я")
    email = forms.EmailField(label="Електронна пошта")
    message = forms.CharField(widget=forms.Textarea ,label="Ваше повідомлення")
