from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


class SingUpView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'authentication/signup.html', context={'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            auth_user = authenticate(request,
                                     username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if auth_user is not None:
                login(request, auth_user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            return redirect(settings.LOGIN_URL)
        else:
            return render(request, 'authentication/signup.html', context={'form': form})

