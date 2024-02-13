from django.shortcuts import render 
from .models import *
import random
import requests
# Create your views here.

def index(request):
    return render(request,"index.html")

def product(request):
    return render(request,"product.html")

def blog(request):
    return render(request,"blog.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg1 = "Email is Already register"
            return render(request,"signup.html",{'msg1':msg1})
        
        except:
                if request.POST['password']==request.POST['cpassword']:
                    User.objects.create(
                        email = request.POST['email'],
                        firstname = request.POST['firstname'],
                        lastname = request.POST['lastname'],
                        mobile = request.POST['mobile'],
                        password = request.POST['password']
                    )
                    msg = "Signup Successfully"
                    return render(request,'login.html',{'msg':msg})
                else:
                    msg1 = "Password & confirm password does not match"
                    return render(request,"signup.html",{'msg1':msg1})

    else:
        return render(request,"signup.html")
        
def login(request):
    if request.method=="POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if user.password == request.POST["password"]:
                request.session['email']=user.email
                request.session['firstname']=user.firstname
                return render(request,"index.html")

            else:
                msg1 = "email and Password doesn't match"
                return render(request,"login.html",{'msg1':msg1})
            
        except:
            msg1 = "email does not registered"
            return render(request,"signup.html",{'msg1':msg1})

    return render(request,"login.html")

def logout(request):
    del request.session['email'],
    del request.session['firstname'],
    return render(request,"logout.html")

def fpass(request):
    if request.method=="POST":
        try:
            User.objects.get(mobile=request.POST['mobile'])
            mobile = request.POST['mobile']
            otp = random.randint(1001,9999)
            url = "https://www.fast2sms.com/dev/bulkV2"

            querystring = {"authorization":"hoCmpbSYJTELXt7rfBwMqcK6x89FlZGvN1aukgHO3iDedQWjVUVzCow5IjOhvN7a90xAnq1pHJrYmSfP","variables_values":str(otp),"route":"otp","numbers":str(mobile)}

            headers = {
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            print(response.text)
            return render(request,"otp.html")
        except:
            return render(request,"fpass.html")
        
    else:
        return render(request,"fpass.html")
        
def otp(request):
    return render(request,"otp.html")

def shopping_cart(request):
    return render(request,"shoping_cart.html")