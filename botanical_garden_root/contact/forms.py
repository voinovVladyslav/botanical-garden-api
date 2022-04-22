from django import forms

class ContactForm(forms.Form):
    user_name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': "Ім'я:"}))
    phone_number = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder': 'Номер телефону:'}))
    user_email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'E-Mail:'}))
    user_message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Повідомлення:'}))
