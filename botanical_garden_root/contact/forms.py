from django import forms

class ContactForm(forms.Form):
    user_name = forms.CharField(max_length=100, label="Ім'я: ")
    phone_number = forms.IntegerField(label = "Номер телефону: ")
    user_email = forms.EmailField(label="E-Mail: ")
    user_message = forms.CharField(widget=forms.Textarea, label="Повідомлення: ")
