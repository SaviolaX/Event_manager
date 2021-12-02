from django.shortcuts import render, redirect

from .models import Profile
from .forms import UserRegistrationForm, EditProfileForm, EditUserForm


def register(request):
    """ Registration user to the database """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)

            context = {'new_user': new_user}
            return render(request, 'accounts/register_done.html', context)
    else:
        user_form = UserRegistrationForm()

    context = {'user_form': user_form}
    return render(request, 'accounts/register.html', context)


def edit_current_profile_account(request, id):
    """Edit user's profile"""
    form = EditProfileForm(instance=request.user.profile)
    user_form = EditUserForm(instance=request.user)

    if request.method == 'POST':
        user_form = EditUserForm(instance=request.user,
                                 data=request.POST)
        form = EditProfileForm(request.POST, request.FILES,
                               instance=request.user.profile)
        if form.is_valid() and user_form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            user_form.save()
            return redirect('accounts:profile', profile.id)
    else:
        form = EditProfileForm(instance=request.user.profile)
        user_form = EditUserForm(instance=request.user)

    context = {'form': form, 'user_form': user_form}
    return render(request, 'accounts/edit_profile.html', context)
