from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
def register(request): 
    if request.method == 'POST':
       # Get form values
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       password2 = request.POST['password2']

       # Check if passwords match
       if password == password2:
          # Check username
          if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is taken')
            return redirect('accounts:register')
          else:
            if User.objects.filter(email=email).exists():
               messages.error(request, 'That email is being used')
               return redirect('accounts:register')
            else:
              # Looks good
              user = User.objects.create_user(username=username, password=password, email=email,
              first_name=first_name, last_name=last_name)
              # Login after register 
              # auth.login(request, user)
              # message.success(request, 'You are now logged in')
              # return redirect('index')
              user.save()
              messages.success(request, 'You are now registered and can log in')
              return redirect('accounts:login')
       else:
         messages.error(request, 'Password do not match')
         return redirect('accounts:register')
    else:
       return render(request, 'accounts/register.html')

def login_view(request): 
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']

      user = auth.authenticate(username=username, password=password)

      if user is not None:
         auth.login(request, user)
         messages.success(request, 'You are now logged in')
         return redirect('accounts:dashboard')
      else:
        messages.error(request, 'Invalid credentials')
        return redirect('accounts:login')
    else:
       return render(request, 'accounts/login.html')

def logout_view(request): 
    if request.method == 'POST':
      auth.logout(request)
      messages.success(request, 'You are now logged out')
      return redirect('index')

def dashboard(request): 
   user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

   context = {
      'contacts': user_contacts
   }
   return render(request, 'accounts/dashboard.html', context)