from django.shortcuts import render
from django.contrib.auth.forms import (UserCreationForm,)
from django.urls import (reverse_lazy,)
from django.views.generic import (CreateView,)


# class MyUserCreationForm(UserCreationForm):
#
#     class Meta:
#         fields = ("username", "email",)


class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm  #MyUserCreationForm
    success_url = reverse_lazy('index')

