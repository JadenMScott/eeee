from __future__ import unicode_literals
from django.shortcuts import render
from django.db import models
import re,bcrypt,datetime
# Create your models here.
class UserManager(models.Manager):
    def register_validate(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['reg_email']):
            errors['email'] = ("Invalid email address!")
        if User.objects.filter(email=postData['reg_email']):
            errors['email']='Email recongnized. Please login with your password'
        if len(postData['reg_first_name'])<1:
            errors['first.name']="First name should be at least one character!"
        if len(postData['reg_last_name'])<1:
            errors['last.name']="Last name should be at least one character!"
        if len(postData['reg_email'])<4:
            errors['email']="Email should be at least 4 characters!"
        if len(postData['reg_pass'])<10:
            errors['password']="Password should be at least 8 characters!"
        if postData['reg_pass']!=postData['reg_conf_pass']:
            errors['password']="Passwords must match!"
        return errors
    def login_validate(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['log_email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['log_pass'])<10:
            errors['password']="Password should be at least 10 characters!"
        user = User.objects.filter(email=postData['log_email'])
        if not user:
            errors['email']=("Invalid email address!")
        else:
            logged_user=user[0]
            if bcrypt.checkpw(postData['log_pass'].encode(),logged_user.pw_hash.encode())==False:
                errors['password']="Invalid Password!"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    pw_hash=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

    def __repr__(self):
        return f"{self.first_name},{self.last_name},{self.email}"

class TripManager(models.Manager):
    def trip_validate(self,postData):
        errors={}
        if len(postData['add_destination'])<1:
            errors['add.destination']="Destination should be at least one character!"
        if str(datetime.datetime.now()) >= postData['add_departure']:
            errors['add.departure']="Depature should be in the future!"
        if str(datetime.datetime.now()) >= postData['add_arrival']:
            errors['add.arrival']="Arrival should be in the future!"
        if postData['add_arrival']<postData['add_departure']:
            errors['add.arrival']="Did you invent time travel? If not, don't have your trip end before it begins!🙄"
        return errors

class Trip(models.Model):
    destination=models.CharField(max_length=255)
    traveler=models.ManyToManyField(User,related_name="wants_to_travel")
    plan=models.CharField(max_length=500)
    departure=models.DateTimeField()
    arrival=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    creator=models.ForeignKey(User,related_name="created_trip")
    objects=TripManager()

    def d_date(self):
        return self.departure.strftime('%B %d %Y')
    def a_date(self):
        return self.arrival.strftime('%B %d %Y')

    def __repr__(self):
        return f"{self.destination},{self.taveler},{self.plan},{self.departure},{self.arrival}"
