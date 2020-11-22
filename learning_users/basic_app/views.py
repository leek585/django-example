from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
#if you want a view that requires the user to login
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpsResponse("You are logged in, Nice!")
#this decorator ensure user is logged in before it can be logged out
@login_required
def user_logout(request):
    #logs out the user
    logout(request)
    return render(request,'basic_app/index.html')

def register(request):

    registered= False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #save user form to database
            user = user_form.save()
            #hash the password
            user.set_password(user.password)
            #save hashed password
            user.save()

            # dont want to commit to database yet
            profile=profile_form.save(commit=False)
            #one-to-one relationship
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        #forms invalid
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})





def user_login(request):
    #submitted something
    if request.method == 'POST':
        #Get from that POST username
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                #reverse and redirect them to homepage
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpsResponse("invalid login details supplied")
    else:
        return render(request,'basic_app/login.html',{})
