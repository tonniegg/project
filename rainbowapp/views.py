from django.shortcuts import render,redirect,get_object_or_404
from .models import Album
from .forms import AlbumForm,SongForm,UserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='rainbowapp:login')
def index(request):
    albums =Album.objects.filter(user=request.user)
    context ={
        'albums':albums
    }
    return render(request,'rainbowapp/index.html',context)

def details(request,album_id):
    album =get_object_or_404(Album,pk=album_id)
    return render(request,'rainbowapp/details.html',{'album':album})

@login_required(login_url='rainbowapp:login')
def add_album(request):
    form=AlbumForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        album=form.save(commit=False)
        album.cover=request.FILES['cover']
        album.user=request.user
        album.save()
        return render(request,'rainbowapp/details.html',{'album':album})
    return render(request,'rainbowapp/add_album.html',{'form':form})

def add_song(request,album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album =get_object_or_404(Album,pk=album_id)
    if form.is_valid():
        song=form.save(commit=False)
        song.audio=request.FILES['audio']
        song.album=album
        song.save()

        return render(request,'rainbowapp/details.html',{'album':album})
    return render(request, 'rainbowapp/add_song.html', {'form': form})

def delete_album(request,album_id):
    album =get_object_or_404(Album,pk=album_id)
    album.delete()
    return redirect('rainbowapp:index')

def signup(request):
    form=UserForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        user=form.save(commit=False)
        user.set_password(password)
        user.save()
        user=authenticate(username=username,password=password)
        login(request,user)
        return redirect('rainbowapp:index')
    return render(request, 'rainbowapp/signup.html', {'form': form})

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        login(request,user)
        return redirect('rainbowapp:index')
    return render(request, 'registration/login.html')

def logout_user(request):
    logout(request)
    return redirect('rainbowapp:login')







