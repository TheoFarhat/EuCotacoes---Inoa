from django import forms
from .models import User, Asset
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    name = forms.CharField(label='Nome', max_length=50, widget=forms.TextInput(attrs={'class': 'forms-style'}))
    age = forms.IntegerField(label='Idade', widget=forms.NumberInput(attrs={'class': 'forms-style'}))
    cpf = forms.IntegerField(label='CPF', widget=forms.TextInput(attrs={'placeholder': 'Digite apenas números', 'class': 'forms-style'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'forms-style'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'forms-style'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'age', 'cpf', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Cadastrar', css_class='button'))
        self.helper.label_class = 'names-form'
        self.helper.error_text_inline = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Login', css_class='button-login'))
        self.helper.label_class = 'names-form-login'
        self.helper.error_text_inline = False
        self.fields['username'].widget.attrs['class'] = 'forms-style-login'
        self.fields['password'].widget.attrs['class'] = 'forms-style-login'


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
