from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from django import forms
# from django.core.validators import *

class regcontrol(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = "First Name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last Name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        if len(postData['pw']) < 8:
            errors["pw"] = "Password should be at least 8 characters"
        if postData['pw'] != postData['cpw']:
            errors['checkpw'] = 'Passwords do not match!'
        return errors


class Users(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    email = models.EmailField()
    pw = models.CharField(max_length=200)
    # confirmpw = models.CharField(max_length=200)
    objects = regcontrol()
    
class authors(models.Model):
    name = models.CharField(max_length=20)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)
    

class books(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(Users, related_name='books', on_delete=models.CASCADE)
    author = models.ForeignKey(authors, related_name='books', on_delete=models.CASCADE)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)
    
class rating(models.Model):
    rating = models.CharField(max_length=5)
    review = models.TextField(max_length=30)
    books = models.ForeignKey(books, related_name='rating', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='rating', on_delete=models.CASCADE)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)



    


# Create your models here.
