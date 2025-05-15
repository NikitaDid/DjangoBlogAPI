from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from apps.user.froms import LoginForm


def user_login(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('index')
        error = 'Wrong Login or Password'
    return render(request, 'user/login.html', {'error':error})
