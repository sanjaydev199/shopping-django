# from django.contrib.auth import authenticate, login,logout
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.conf import settings
# from datetime import timedelta
# from django.contrib.auth.decorators import login_required
# from shoppingapp.models import CustomUser, RegUsers
# from django.contrib.auth import get_user_model
# from django.db import IntegrityError
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import random
# from django.utils import timezone
# from django.db.models import Q
# from django.shortcuts import render, get_object_or_404
# from django.db.models import Count
# User = get_user_model() 


# def SIGNUP(request):
#     if request.method == "POST":        
#         pic = request.FILES.get('profile_pic')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         mobilenumber = request.POST.get('mobilenumber')        
#         password = request.POST.get('password')

#         if CustomUser.objects.filter(email=email).exists():
#             messages.warning(request, 'Email already exists')
#             return redirect('signup')
#         if CustomUser.objects.filter(username=username).exists():
#             messages.warning(request, 'Username already exists')
#             return redirect('signup')
#         else:
#             user = CustomUser(
#                 first_name=first_name,
#                 last_name=last_name,
#                 username=username,
#                 email=email,
#                 user_type=2,
#                 profile_pic=pic,
#             )
#             user.set_password(password)
#             user.save()          

#             reguser = RegUsers(
#                 admin=user,
#                 mobilenumber=mobilenumber,
                
#             )
#             reguser.save()
#             messages.success(request, 'You signup Successfully')
#             return redirect('signup')
#     return render(request,'customer/signup.html')


# login_required(login_url='/')
# def Setting(request):
#      context ={}
#      ch = User.objects.filter(id = request.user.id)
     
#      if len(ch)>0:
#             data = User.objects.get(id = request.user.id)
#             context["data"]:data            
#      if request.method == "POST":        
#         current = request.POST["cpwd"]
#         new_pas = request.POST['npwd']
#         user = User.objects.get(id = request.user.id)
#         un = user.username
#         check = user.check_password(current)
#         if check == True:
#           user.set_password(new_pas)
#           user.save()
#           messages.success(request,'Password Change  Succeesfully!!!')
#           user = User.objects.get(username=un)
#           login(request,user)
#         else:
#           messages.success(request,'Current Password wrong!!!')
#           return redirect("setting")
#      return render(request,'customer/setting.html')

# @login_required(login_url = '/')
# def USER_PROFILE(request):
#     reguser = RegUsers.objects.get(admin = request.user.id)
#     context = {
#         "ru":reguser,
#     }
#     return render(request,'customer/user-profile.html',context)



# @login_required(login_url='/')
# def USER_PROFILE_UPDATE(request):
#     if request.method == "POST":
#         # Fetching user ID from the session or POST data, not FILES
#         user_id = request.user.id  # This assumes you want to update the currently logged-in user
#         profile_pic = request.FILES.get('profile_pic')  # Image upload
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         mobilenumber = request.POST.get('mobilenumber')
#         email = request.POST.get('email')

#         try:
#             # Get the registered user instance
#             reguser = RegUsers.objects.get(admin=user_id)
#             customuser = reguser.admin  # Assuming 'admin' is a ForeignKey to the CustomUser model

#             # Updating user information
#             customuser.first_name = first_name
#             customuser.last_name = last_name
#             customuser.email = email            
#             reguser.mobilenumber = mobilenumber

#             # Update profile picture if it exists
#             if profile_pic:
#                 customuser.profile_pic = profile_pic

#             # Save the updated information
#             customuser.save()
#             reguser.save()

#             # Success message and redirect
#             messages.success(request, "Your profile has been updated successfully")
#             return redirect('user_profile')

#         except RegUsers.DoesNotExist:
#             messages.error(request, "User not found")
#         except Exception as e:
#             messages.error(request, f"Profile update failed: {e}")

#     return render(request, 'customer/user-profile.html')



from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shoppingapp.models import CustomUser, RegUsers
from django.contrib.auth import get_user_model

User = get_user_model()


# ---------------- SIGNUP ----------------

def SIGNUP(request):
    if request.method == "POST":        
        pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')        
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('signup')

        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=2,
            profile_pic=pic,
        )
        user.set_password(password)
        user.save()

        # Profile create
        RegUsers.objects.create(
            admin=user,
            mobilenumber=mobilenumber,
        )

        messages.success(request, 'You signup Successfully')
        return redirect('signup')

    return render(request,'customer/signup.html')


# ---------------- SETTING ----------------

@login_required(login_url='/')
def Setting(request):
    context = {}

    data = User.objects.filter(id=request.user.id).first()
    if data:
        context["data"] = data   # ✅ FIX

    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']

        user = User.objects.get(id=request.user.id)
        un = user.username

        if user.check_password(current):
            user.set_password(new_pas)
            user.save()

            messages.success(request,'Password Changed Successfully!!!')

            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.error(request,'Current Password wrong!!!')
            return redirect("setting")

    return render(request,'customer/setting.html', context)


# ---------------- USER PROFILE ----------------

@login_required(login_url='/')
def USER_PROFILE(request):

    reguser = RegUsers.objects.filter(admin=request.user).first()

    # AUTO CREATE if missing
    if reguser is None:
        reguser = RegUsers.objects.create(admin=request.user)

    context = {
        "ru": reguser,
    }

    return render(request,'customer/user-profile.html', context)


# ---------------- PROFILE UPDATE ----------------

@login_required(login_url='/')
def USER_PROFILE_UPDATE(request):

    if request.method == "POST":

        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobilenumber = request.POST.get('mobilenumber')
        email = request.POST.get('email')

        reguser = RegUsers.objects.filter(admin=request.user).first()

        if reguser is None:
            reguser = RegUsers.objects.create(admin=request.user)

        customuser = reguser.admin

        # update data
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.email = email
        reguser.mobilenumber = mobilenumber

        if profile_pic:
            customuser.profile_pic = profile_pic

        customuser.save()
        reguser.save()

        messages.success(request, "Your profile has been updated successfully")
        return redirect('user_profile')

    return render(request, 'customer/user-profile.html')

def SIGNUP(request):
    if request.method == "POST":
        pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        password = request.POST.get('password')

        # ADD THIS BLOCK
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            user_type=2,
            profile_pic=pic
        )

        RegUsers.objects.create(
            admin=user,
            mobilenumber=mobilenumber
        )

        messages.success(request, "Signup Successfully")
        return redirect('signup')

    return render(request,'customer/signup.html')