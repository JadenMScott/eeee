
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'eeee_app/index.htm')
def register(request):
    if request.method=="POST":
        errors = User.objects.register_validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            print(request.POST)
            firstname=request.POST['reg_first_name']
            lastname=request.POST['reg_last_name']
            email=request.POST['reg_email']
            password=request.POST['reg_pass']
            password_confirm_=request.POST['reg_conf_pass']
            if password!=password_confirm_:
                messages.error(request, "Passwords must match")
                return redirect('/')
            else:
                pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                print(pw_hash)
                User.objects.create(first_name=firstname, last_name=lastname, email=email, pw_hash=pw_hash)
                newUser=User.objects.last()
                print(newUser)
                request.session['logged_user']= newUser.id
                request.session['first_name']= newUser.first_name
                request.session['email']=newUser.email
                return redirect(f"/dashboard/{newUser.id}")
        return redirect("/")
def login(request):
    if request.method == "GET":
        return render(request,'book_app/index.htm')
    elif request.method == "POST":
        errors = User.objects.login_validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    # errors = User.objects.login_validate(request.POST)
        else:
            user = User.objects.filter(email=request.POST['log_email'])
            if len(user)>0:
                print (user[0])
                logged_user=user[0]
                if bcrypt.checkpw(request.POST['log_pass'].encode(),logged_user.pw_hash.encode())==True:
                    print("password match")
                    request.session['logged_user']= logged_user.id
                    request.session['first_name']= logged_user.first_name
                    request.session['email']= logged_user.email
                    # request.session['user']=logged_user
                    # request.session['userid']=logged_user.id
                    return redirect(f"/dashboard/{logged_user.id}")
                else:
                    print("Invalid password. Please try again")
            else:
                print("User not found. Please register today!")
            return redirect("/")
def add_trip(request):
    if 'first_name' not in request.session:
        return render(request,'eeee_app/yikes.htm')
    else:
        if request.method=="POST":
            errors = Trip.objects.trip_validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/add_trip')
            else:
                view_destination=request.POST['add_destination']
                view_departure=request.POST['add_departure']
                view_arrival=request.POST['add_arrival']
                view_plan=request.POST['add_plan']
                # view_traveler=request.session['logged_user']
                creator=User.objects.filter(email=request.session['email'])[0]
                user=User.objects.get(first_name=request.session['first_name'])
                Trip.objects.create(destination=view_destination,creator=user,departure=view_departure,arrival=view_arrival,plan=view_plan)
                t=Trip.objects.last()
                t.traveler.add(creator)
                t.save()
                return redirect(f"/dashboard/{creator.id}")
        else:
            request.session['id']=User.objects.get(first_name=request.session['first_name']).id
            context={
                'first_name':User.objects.get(first_name=request.session['first_name']),
                'destination':Trip.destination
            }
            return render(request,'eeee_app/add_trip.htm',context)
def dashboard(request,id):
    if 'first_name' in request.session:
        if request.method=="GET":
            first_name=User.objects.filter(first_name=request.session['first_name'])
            user_first_name=first_name[0]
            context={
                'user':User.objects.get(id=id),
                'logged_user':Trip.objects.filter(traveler=user_first_name),
                'not_logged_user':Trip.objects.exclude(traveler=user_first_name),

            }
            return render(request,'eeee_app/dashboard.htm',context)
    else:
        return render(request,'eeee_app/yikes.htm')
def trip(request,id):
    if 'first_name' not in request.session:
        return render(request,'eeee_app/yikes.htm')
    else:
        # not_id=Trip.objects.get(id=id).traveler
        context={
            'trip':Trip.objects.get(id=id),
            # 'traveler'
        }
        return render(request,'eeee_app/trip.htm',context)
def edit_trip(request,id):
    if 'first_name' not in request.session:
        return render(request,'eeee_app/yikes.htm')
    else:
        if request.method=="POST":
            errors = Trip.objects.trip_validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/add_trip')
            else:
                trip=Trip.objects.get(id=id)
                trip.destination=request.POST['add_destination']
                trip.deaprture=request.POST['add_departure']
                trip.arrival=request.POST['add_arrival']
                trip.plan=request.POST['add_plan']
                trip.save()
                # view_traveler=request.session['logged_user']
                creator=User.objects.filter(email=request.session['email'])[0]
                return redirect(f"/dashboard/{creator.id}")
        else:
            request.session['id']=User.objects.get(first_name=request.session['first_name']).id
            context={
                'first_name':User.objects.get(first_name=request.session['first_name']),
                'destination':Trip.destination
            }
            return render(request,'eeee_app/add_trip.htm',context)
def join(request,id):
    user=User.objects.get(first_name=request.session['first_name'])
    trip=Trip.objects.get(id=id)
    trip.traveler.add(user)
    trip.save()
    creator=User.objects.filter(email=request.session['email'])[0]
    return redirect(f"/dashboard/{creator.id}")
def cancel(request,id):
    user=User.objects.get(first_name=request.session['first_name'])
    trip=Trip.objects.get(id=id)
    trip.traveler.remove(user)
    trip.save()
    creator=User.objects.filter(email=request.session['email'])[0]
    return redirect(f"/dashboard/{creator.id}")
def remove(request,id):
    trip=Trip.objects.get(id=id)
    trip.delete()
    creator=User.objects.filter(email=request.session['email'])[0]
    return redirect(f"/dashboard/{creator.id}")
def logout(request):
    request.session.clear()
    return redirect("/")