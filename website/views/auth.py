from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from ..forms import SignUpForm

# Create your views here.
def home(request):
    return render(request,'home.html',{})
def login_user(request):
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
            return redirect('login')
    return render(request,'login.html')


def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('login')

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
            # request.session['info'] ={'username':username,'password':password} 
            messages.success(request,'You have successfully registered')
            return redirect('home')
        else:
            messages.success(request,'There was an error registering, please try again')
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})





# def add_message(request, message, level):
#     print(message,level)
#     if level == 'error':
#         messages.error(request, message)
#     elif level == 'success':
#         messages.success(request, message)
#     elif level == 'warning':
#         messages.warning(request, message)
#     elif level == 'info':
#         messages.info(request, message)
#     return JsonResponse({'status': 'ok'})




    