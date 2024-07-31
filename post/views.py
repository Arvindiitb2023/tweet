from django.shortcuts import render , redirect,get_object_or_404
from .models import Tweet
from .forms import Tweetform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

# Create your views here.

def index(request):
    return render(request , 'index.html')

def home(request):
   if request.user.is_authenticated:
         form = Tweetform(request.POST or None)
         if request.method == 'POST': 
          if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            return redirect('home')
         tweets = Tweet.objects.all().order_by("-created_at")
         return render(request , 'home.html' ,{'tweets':tweets ,'form':form})  
     
   else:
      tweets = Tweet.objects.all().order_by("-created_at")
      return render(request , 'home.html' ,{'tweets':tweets})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('register')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# def delete(request,pk):
#      if request.user.is_authenticated:
#          tweet = get_object_or_404(Tweet,id=pk)

def edit(request, pk):
    tweet = get_object_or_404(Tweet ,id =pk , user = request.user)
    if request.method =='POST':
        form = Tweetform(request.POST ,request.FILES,instance=tweet)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            return redirect('home')
    else:
        form = Tweetform(instance=tweet)
    return render(request,'home.html' ,{'form':form})

def delete(request,pk):
    tweet = get_object_or_404(Tweet ,id =pk , user = request.user)
    if request.method =='POST':
        tweet.delete()
        return redirect('home')
    return render(request,'delete.html' ,{'tweet':tweet})