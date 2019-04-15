from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
import re

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    # print('inside register method in views')
    result = User.objects.reg_validator(request.POST)
    # print('back inside register in views')
    # print(result)
    if len(result) > 0:
        for key, value in result.items():
            # messages.error(request, value)
            messages.add_message(request, messages.ERROR, value)
        return redirect('/')
    else:  # passed validations
        # create the user (add to database)
        hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'],
        email=request.POST['email'], birthday=request.POST['birthday'], password=hash.decode())
        # print(user.id)
        # save their id in session
        request.session['userid'] = user.id
        # redirect to addmovie page/dashboard
        return redirect('/displaysong')

def displaysong(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['userid'])
        songs = user.songFavorites.all()
        unfavorites = []
        allsongs = Song.objects.all()
        for i in allsongs:
            if i not in songs:
                unfavorites.append(i)
        context = {
            'user': user,
            'songs': songs,
            'unfavorites': unfavorites
        }

        return render(request, 'displaysong.html', context)

def addsong(request):
    context = {
        "artist": Artist.objects.all()
        }
    return render(request, 'addsong.html', context)

def addartist(request):
# context = {
#     "song": Song.objects.get
# }
    return render(request, 'addsong.html')

def createsong(request):
    user = User.objects.get(id=request.session['userid'])
    if len(request.POST['new']) < 1:
        artist = Artist.objects.get(id=request.POST['existing'])

    else:
       artist = Artist.objects.create(addedby=user, artistname=request.POST['new'])
    Song.objects.create(title=request.POST['title'], artist=artist, addedby=user)
    newSong = Song.objects.last()
    favorite(request, newSong.id)
    return redirect('/addsong')

def delete(request, id):
    song = Song.objects.get(id=id)
    song.delete()
    return redirect('/displaysong')

def favorite(request, id):
    user = User.objects.get(id=request.session['userid'])
    song = Song.objects.get(id=id)
    user.songFavorites.add(song)
    return redirect('/displaysong')

def favoriteartist(request,id):
    user = User.objects.get(id=request.session['userid'])
    artist = Artist.objects.get(id=id)
    user.artistFavorites.add(artist)
    return redirect('/displaysong')


def unfavorite(request, id):
    user = User.objects.get(id=request.session['userid'])
    song = Song.objects.get(id=id)
    user.songFavorites.remove(song)
    return redirect('/displaysong')

def showsong(request, id):
    song = Song.objects.get(id=id)
    context = {
        "song": song,
        "favorites": Song.objects.get(id=id).favorites.all(),
        "artist": Artist.objects.filter(songs=song)
    }
    return render(request, "showsong.html", context)

def showartist(request, id):
    artist = Artist.objects.get(id=id)
    context = {
        "artist": artist,
        "favorites": Artist.objects.get(id=id).favorites.all(),
        "songs" : artist.songs.all()
    }
    return render(request, "showartist.html", context)

def login(request):
    result = User.objects.loginvalidator(request.POST)
    if len(result) > 0:
        for key, value in result.items():
            messages.add_message(request, messages.ERROR, value)
        return redirect('/')
    else:
        user = User.objects.get(
            username=request.POST['username'], email=request.POST['email'])
        request.session['userid'] = user.id
        return redirect('/displaysong')

def logout(request):
    request.session.clear()
    return redirect('/')

