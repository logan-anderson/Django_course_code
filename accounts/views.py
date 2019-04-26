from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contact.models import contact as Contact


def register(request):
    if request.method == 'POST':
        # Register User

        #Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        pass_1 = request.POST['password']
        pass_2 = request.POST['password2']

        # Check if passwords match
        if pass_1 == pass_2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already in use')
                    return redirect('register')
                else:
                    # everytihng looks good
                    user = User.objects.create_user(username=username, password=pass_1, email=email, first_name=first_name, last_name=last_name)
                    # Login the user
                    # auth.login(request, user)
                    # messages.success(request, 'Now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'Now registered and can log in')
                    return redirect('login')
            return
        else:
            messages.error(request, 'Passwords to not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        # POST
        # Login User
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect password or username')
            return redirect('login')
    else:
        # GET
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        #POST
        auth.logout(request)
        messages.success(request, 'you are now logged  out')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.filter(user_id=request.user.id).order_by('-contact_date')
    context = {
        'contacts': user_contacts,

    }
    return render(request, 'accounts/dashboard.html', context)
