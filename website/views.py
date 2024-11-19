from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Custom
from .forms import SignUpForm,AddRecordForm
# Create your views here.
def home(request):
    customs=Custom.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have been logged in')
            return redirect('home')
        else:
            messages.success(request,'There was an error logging in, please try again')
            return redirect('home')
    return render(request,'home.html',{'customs':customs})

# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'You have successfully registered')
            return redirect('home')
        else:
            messages.success(request,'There was an error registering, please try again')
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})

def custom_record(request,pk):
    if request.user.is_authenticated:
        custom=Custom.objects.get(id=pk)
        return render(request,'record.html',{'custom':custom})
    else:
        messages.success(request,'You must be logged in to view that page')
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Custom.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Record deleted successfully')
        return redirect('home')
    else:
        messages.success(request,'You must be logged in to view that page')
        return redirect('home')
    

def add_record(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid():
                add_record=form.save()
                messages.success(request,'Record added successfully')
                return redirect('home')
        else:
            form = AddRecordForm()
            return render(request,'add_record.html',{'form':form})
    return render(request,'add_record.html',{})

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record=Custom.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,'Record updated successfully')
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
