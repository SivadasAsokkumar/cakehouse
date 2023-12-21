from django import forms
from cakeapp.models import User,Category,Cakes,CakeVarients,Offers,Orders
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2","phone","address"]
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    widgets={
        "username":forms.TextInput(),
        "password":forms.PasswordInput()
    }


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name"]


class CakeAddForm(forms.ModelForm):
    class Meta:
        model=Cakes
        fields=["name","flavour","image","Category"]


class CakeVarientForm(forms.ModelForm):
    class Meta:
     model=CakeVarients
     exclude=("cake",)


class OfferAddForm(forms.ModelForm):
    class Meta:
        model=Offers
        exclude=("cakevarient",)
        widgets={
            "start_date":forms.DateInput(attrs={"type":"date"}),
            "due_date":forms.DateInput(attrs={"type":"date"})
        }

class OrderChangeForm(forms.ModelForm):
    class Meta:
        model=Orders
        exclude=("user","cakevarient","orderd_date","address")
        widgets={
            "expected_date":forms.DateInput(attrs={"type":"date"}),
            "status":forms.TextInput()
        }
