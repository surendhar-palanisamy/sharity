from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
# YEARS = [x for x in range(1940, 2021)]
#     dob = forms.DateField(
#         label='What is your birth date?', widget=forms.SelectDateWidget(years=YEARS))


class CreateUserForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update(
    #         {'placeholder': ('Username')})
    #     self.fields['email'].widget.attrs.update({'placeholder': ('Email')})
    #     self.fields['password1'].widget.attrs.update(
    #         {'placeholder': ('Password')})
    #     self.fields['password2'].widget.attrs.update(
    #         {'placeholder': ('Repeat password')})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DateInput(forms.DateInput):
    input_type = 'date'


class Profilemodelform(forms.ModelForm):

    dp = forms.ImageField(label=('display picture'), required=False, error_messages={
                          'invalid': ("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'mobile_number', 'dp', 'payment_password', 'dob']
        widgets = {
            'dob': DateInput(),
        }


class Postcreationform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text_area', 'cash_required', 'documents']
        widgets = {
          'text_area': forms.Textarea(attrs={'rows':4, 'cols':28}),
          'cash_required':forms.Textarea(attrs={'rows':1, 'cols':28})
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['cash']
