from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from users.models import CustomUser
from users.forms import UserCreateForm,UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class RegisterView(View):
    def get(self,request):
        create_form = UserCreateForm()
        context = {
            'form':create_form
        }
        return render(request,'users/register.html',context)


    def post(self,request):
        create_form  = UserCreateForm(data=request.POST)
        
        if create_form.is_valid():
            create_form.save()
        else: 
            context = {
            'form':create_form
        }
            return render(request,'users/register.html',context)

        #create user account
        return redirect('users:login')

class LoginView(View):
    def get(self,request):
        login_form = AuthenticationForm()
        context={
            "form":login_form
        }
        return render(request,'users/login.html',context)

    def post(self,request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request,user)
            messages.success(request,"You have successfully logged in")
            return redirect('list')

        else:
            context={"form":login_form}
        return render(request,'users/login.html',context)


        context={
            "form":login_form
        }
        return render(request,'users/login.html',context)


class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        context={
            "user":request.user
        }
        return render(request,'users/profile.html',context)


class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.info(request,"You have successfully logged out")
        return redirect("landing_page")


class ProfileUpdateView(LoginRequiredMixin,View):
    def get(self,request):  
        user_update_form = UserUpdateForm(
            instance=request.user
            )
        context={
            "form":user_update_form,
        }  
        return render(request,
        'users/profile_edit.html',context)


    def post(self,request):
        user_update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files = request.FILES
            )

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request,"You have successfully updated your profile")

            return redirect('users:profile')

        else:
            return render(request,'users/profile-edit.html',{"form":user_update_form})


