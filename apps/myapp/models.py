from django.db import models
import re
import datetime
import bcrypt


class UserManager(models.Manager):
    def reg_validator(self, form):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$")

        fname = form['fname']
        lname = form['lname']
        email = form['email']
        birthday = form['birthday']
        password = form['password']
        confirm_pw = form['confirm_password']
        print(birthday)
        if len(fname) < 2:
            errors['fname'] = "First name cannot be blank"
        elif not fname.isalpha():
            errors['fname'] = "First name cannot contain number or special characters!"
        if len(lname) < 2:
            errors['lname'] = "Last name cannot be blank"
        elif not lname.isalpha():
            errors['lname'] = "Last name cannot contain number or special characters!"
        if len(email) < 1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(email):
            errors["email"] = "Invalid email format"
        else:
            users = User.objects.filter(email=email)
            if len(users) > 0:
                errors['email'] = "Email already exists. Please login."
        if not birthday:
            errors['birthday'] = "Please enter a birth date"
        elif birthday > str(datetime.datetime.now()):
            errors['birthday'] = "Sorry you don't exist"
        elif datetime.datetime.now()-datetime.datetime.strptime(birthday, "%Y-%m-%d") <= datetime.timedelta(days=4745):
            errors['birthday'] = "You are too young for mature lyrics"
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif password != confirm_pw:
            errors['confirm_pw'] = "Passwords do not match"

        return errors

    def loginvalidator(self, form):
        errors = {}
        email = form['email']
        password = form['password']
        if len(email) < 0:
            errors["email"] = "Please enter emails"
        elif len(User.objects.filter(email=email)) < 1:
            errors['email'] = "Email not in database please register!"
        else:
            if not bcrypt.checkpw(password.encode(), User.objects.get(email=email).password.encode()):
                errors['email'] = "invald email!"

        return errors


class SongManager(models.Manager):
    def song_validator(self, form):

        errors = {}
        title = form['title']
        if len(title) < 1:
            errors["title"] = "Title cant be blank"
        if len(title) < 2:
            errors["title"] = "Title is too short"
        return errors


class ArtistManager(models.Manager):

    def artist_validator(self, form):
        errors = {}
        title = form['title']
        if len(title) < 2:
            errors["title"] = "Title is too short"
        return errors


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """uploaded_songs get list of uploaded songs for user"""
    """favorites get list of favorited songs for user"""
    objects = UserManager()


class Artist(models.Model):
    artistname = models.CharField(max_length=255)
    addedby = models.ForeignKey(
        User, related_name="songs", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="artistFavorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = SongManager()


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist, related_name="songs", on_delete=models.CASCADE)
    addedby = models.ForeignKey(
        User, related_name="uploaded_songs", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="songFavorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = SongManager()
