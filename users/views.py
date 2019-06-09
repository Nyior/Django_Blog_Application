from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .forms import UserUpdateForm
from .forms import  ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #this saves the form data to the database
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created you are now able to log in!')
            return redirect('login') #redirects the user to the login page.
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):

    if request.method == 'POST':
        context = {
            'u_form': UserUpdateForm(request.POST, instance=request.user),
            'p_form': ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)
        }
        if context['u_form'].is_valid() and context['p_form'].is_valid():
            context['u_form'].save() #this saves the form data to the database
            context['p_form'].save()
            messages.success(request, 'Your profile has beenn updated!')
            return redirect('users-profile') #redirects the user to the profile page.
    else:
        context = {
            'u_form': UserUpdateForm(instance=request.user),
            'p_form': ProfileUpdateForm(instance=request.user.profile)
        }

    return render(request, 'users/profile.html', context)
