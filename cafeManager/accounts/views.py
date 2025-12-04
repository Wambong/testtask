
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from orders.models import Item
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser

def test_view(request):
    items = Item.objects.all()
    return render(request, 'accounts/test.html', {'items': items})
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        remember_me = request.POST.get('remember_me')  # <-- new line

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                # 🔥 Set session expiry
                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
                else:
                    request.session.set_expiry(0)  # Browser close

                messages.success(request, f'Welcome back, {user.full_name or user.email}!')
                return redirect('dashboard')

        messages.error(request, 'Invalid email or password.')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def update_profile_pic(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        request.user.profile_pic = request.FILES['profile_pic']
        request.user.save()
        messages.success(request, 'Profile picture updated successfully!')
    else:
        messages.error(request, 'No image selected for upload.')
    return redirect('profile')

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.is_active = False  # Soft delete
        user.save()

        logout(request)
        messages.success(request, "Your account has been deactivated. We're sorry to see you go.")
        return redirect("login")

    return redirect("profile")

@staff_member_required
def manage_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/manage_users.html', {'users': users})


@staff_member_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot deactivate yourself.")
        return redirect('manage_users')

    user.is_active = not user.is_active
    user.save()

    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User {user.email} has been {status}.")
    return redirect('manage_users')


@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('manage_users')

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('manage_users')

@staff_member_required
def update_user_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        role = request.POST.get("role")

        # Prevent user from editing their own role
        if user == request.user:
            messages.error(request, "You cannot modify your own role.")
            return redirect("manage_users")

        # Update roles
        if role == "admin":
            user.is_staff = True
            user.is_superuser = True
        elif role == "staff":
            user.is_staff = True
            user.is_superuser = False
        else:  # normal user
            user.is_staff = False
            user.is_superuser = False

        user.save()
        messages.success(request, f"Role updated for {user.email}.")
        return redirect("manage_users")

    return redirect("manage_users")




