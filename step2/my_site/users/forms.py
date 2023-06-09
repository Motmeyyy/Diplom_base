# from django import forms
# from django.contrib.auth.models import User, Group
# from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
# from django.contrib.auth.forms import UserChangeForm
# from .models import Appointment
#
#
#
# class UserRegisterForm(UserCreationForm):
#     group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ['username', 'email', 'password1', 'password2','group']
#
# class VerificationForm(forms.Form):
#     verification_code = forms.CharField(max_length=20)
#
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#
# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['full_name', 'polis', 'phone_number', 'heart_rate', 'diet', 'date_of_birth', 'address', 'medical_history', 'image']
#
# class AppointmentForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(AppointmentForm, self).__init__(*args, **kwargs)
#         self.fields['doctor'].queryset = User.objects.filter(groups__name='Мед.персонал')
#         label = 'Врач',
#         empty_label = None,
#         widget = forms.Select(attrs={'class': 'form-control'})
#
#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'date', 'description']
#

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, PurchaseHistory, Diet, Recipe
from .models import Appointment


class UserRegisterForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']


class VerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=20)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'polis', 'phone_number', 'heart_rate', 'diet', 'date_of_birth', 'address', 'medical_history', 'image']


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(groups__name='Мед.персонал')
        self.fields['doctor'].label = 'Врач'
        self.fields['doctor'].empty_label = None
        self.fields['doctor'].widget = forms.Select(attrs={'class': 'form-control'})

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'description']


class DietForm(forms.ModelForm):
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Diet
        fields = ['name', 'description', 'recipes']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients']
