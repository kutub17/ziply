from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth


# Create your views here.


def login(req):
    if not req.user.is_authenticated:
        if req.method == "POST":
            if req.POST['email'] and req.POST['password']:
                try:
                    user = User.objects.get(email=req.POST['email'])
                    auth.login(req, user)

                    if req.POST['next'] != '':
                        return redirect(req.POST['next'])
                    else:
                        return redirect('/')

                except User.DoesNotExists:
                    return redirect(req, login, {"error": "User Doesn't Exists "})
            else:
                return redirect(req, login, {"error": "Empty Fields"})
        else:
            return render(req, 'login.html')
    else:
        return redirect('/')


def signup(req):
    if not req.user.is_authenticated:
        if req.method == "POST":
            if req.POST['password'] == req.POST['password2']:
                if req.POST['username'] and req.POST['email'] and req.POST['password']:
                    try:
                        user = User.objects.get(email=req.POST['email'])
                        return render(req, 'signup.html', {"error": "User Already Exists"})
                    except User.DoesNotExist:
                        User.objects.create_user(
                            username=req.POST['username'],
                            email=req.POST['email'],
                            password=req.POST['password'],
                        )
                        messages.success(req, "Signup Successful")
                        return redirect(login)
                else:
                    return render(req, 'signup.html', {"error": "Empty Fields"})
            else:
                return render(req, 'signup.html', {"error": "Passwords don't match"})

        else:
            return render(req, 'signup.html')

    else:
        return redirect('/')


def logout(req):
    auth.logout(req)
    return redirect(login)
