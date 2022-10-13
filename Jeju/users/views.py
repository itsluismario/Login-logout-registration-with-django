from django.shortcuts import render
from users.models import UserProfile, User

# Create your views here.
from django.contrib.auth import authenticate, logout as do_logout, login as do_login
from users.forms import UserSignUpForm, UserLoginForm
from django.shortcuts import redirect

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required




"""""""""""""""""""""
"""""""Log in"""""""
"""""""""""""""""""""
def user_login(request):
    form = UserLoginForm()
    # If the user is not log in send to "/"
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        
        print(user)
        if user is not None:
            do_login(request,user)
            # Redirect to a success page.
            return redirect("/index")
        else:
            print(user)
            return render(request,'login.html',{
                'form':form,
                'errors': "El correo/contresaña que ingresaste no son los correctos.",
            })

    return render(request,'login.html', {
        'form': form
        })




"""""""""""""""""""""
"""""""Sign Up"""""""
"""""""""""""""""""""
def user_signup(request):

    form = UserSignUpForm()
    # If the user is logged in send to "/"
    if request.method == "POST":
        user_form = UserSignUpForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.email
            user.first_name = user.first_name
            user.last_name = user.last_name
            # If there is not user, create one User model and UserProfile, and save them
            if not User.objects.filter(email = user.email):
                user.set_password(user.password)
                user.save()
                UserProfile.objects.create(User=user)
                do_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                # Redirect to a success page.
                return redirect("/index")
            # If there is one found, send again the form and show an error message
            # There are gonna be two variables in the section of email error. One for the "notUniqueEmail" and 
            # another for general errors "user_form.errors.email"
            elif User.objects.filter(email = user.email):
                return render(request,'signup.html',{
                     'form':form,
                     'notUniqueEmail': "Ya existe un usuario con ese email" 
                })
        else:
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            """""""Future feature: in case the user make a mistake in the form,"""""""""""
            """""""add an option that she does not have to write everything again"""""""""
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            return render(request,'signup.html',{
                'form':form,
                'errors':user_form.errors
            })

    form = UserSignUpForm()
    return render(request,"signup.html",{
        'form': form
    })




""""""""""""""""""""""""
"""Email Verification"""
""""""""""""""""""""""""
def email_verification(request):
    return render(request,"email_verification.html")



""""""""""""
"""Index"""
""""""""""""
def index(request):
    login_user = request.user.is_authenticated
    return render(request,'dashboard.html', {
        'login_user': login_user,
    })
