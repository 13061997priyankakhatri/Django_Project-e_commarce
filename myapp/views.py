from django.shortcuts import render,redirect
from .models import *
import random
import requests
# Create your views here.

def index(request):
        return render(request,"index.html")

def sindex(request):
    return render(request,"sindex.html")

def product(request,cat):
    product=Product()
    if cat=='all':
        product = Product.objects.all()
    elif cat=='women':
        product = Product.objects.filter(pcategory='Women')
    elif cat=='men':
        product = Product.objects.filter(pcategory='Men')
    elif cat=='child':
        product = Product.objects.filter(pcategory='Child')
    return render(request,"product.html",{'product': product})

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
                        password = request.POST['password'],
                        role = request.POST['usertype'],
                        # picture = request.FILES['picture'],
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
                request.session['picture']=user.picture.url
                if user.role == "buyer" :
                    print("hello")
                    return render(request,"index.html")
                else :
                    return render(request,"sindex.html")
            else:
                msg1 = "email and Password doesn't match"
                return render(request,"login.html",{'msg1':msg1})
            
        except:
            msg1 = "email does not registered"
            return render(request,"signup.html")
    else :
        return render(request,"login.html")

def logout(request):
    del request.session['email']
    del request.session['firstname']
    del request.session['picture']
    return render(request,"login.html")

def fpass(request):
    if request.method=="POST":  
        try: 
            User.objects.get(mobile=request.session['mobile'])
            mobile = request.POST['mobile']
            otp = random.randint(1001,9999)
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {"authorization":"tfUafDOabQAXAlemu5vWVAvKtmNvL4JXn57FnWVY0ehGefXQxO8i5AAc5PQL","variables_values":str(otp),"route":"otp","numbers":mobile}
            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            request.session['mobile']=mobile
            request.session['otp']=otp 
            print(mobile)
            print(otp)
            return render(request,"otp.html")
        except:
            return render(request,"fpass.html")    
    else:           
        return render(request,"fpass.html")
        
def otp(request):
    if request.method=="POST":
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        print(type(otp))
        print(type(uotp))

        if otp==uotp:
            print("Hello")
            del request.session['otp']
            return render(request,"newpass.html")
        else:
            print("Hello")
            msg1 = "Invalid Otp"
            return render(request,"otp.html",{'msg1':msg1})
    else:    
        return render(request,"otp.html")
    
def newpass(request):
    if request.method =="POST":
        print("Hello")
        user = User.objects.get(mobile=request.session['mobile'])
        print("Hello")
        if request.POST['newpassword'] == request.POST['cnewpassword']:
            print("Hello")
            user.password = request.POST['newpassword']
            user.save()
            return render(request,"login.html")
        else:
            msg1 = "New password nad Confirm new password does not match"
            return render(request,"newpass.html",{'msg1':msg1,'user':user})            
    else:
        return render(request,"newpass.html")

def shopping_cart(request):
    return render(request,"shoping_cart.html") 

def cpass(request):
    user = User.objects.get(email=request.session['email'])
    if request.method=="POST":
        if user.password==request.POST['oldpassword']:
            if request.POST['newpassword']==request.POST['cnewpassword']:
                user.password = request.POST['newpassword']
                user.save()
                return render(request,'login.html')
            else:
                msg1 = "New password and Confirm new password doesn't match"
                if user.role == "buyer" :
                    return render(request,'cpass.html',{'msg1':msg1})
                else:
                    return render(request,"scpassword.html",{'msg1':msg1})
        else:
            msg1 = "Old password does not match"
            if user.role == "buyer" :
                return render(request,'cpass.html',{'msg1':msg1})
            else:
                return render(request,"scpassword.html",{'msg1':msg1})
    else:
        if user.role == "buyer" :
            return render(request,'cpass.html')
        else:
            return render(request,"scpassword.html")
    
def profile(request):
    user = User.objects.get(email=request.session['email'])
    return render(request,"profile.html",{'user':user})

def add(request):
    seller=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        Product.objects.create(
            seller=seller,
            pcategory=request.POST['pcategory'],
            psize=request.POST['psize'],
            pbrand=request.POST['pbrand'],
            pname=request.POST['pname'],
            desc=request.POST['desc'],
            price=request.POST['price'],
            ppicture=request.FILES['ppicture']               
        )
        msg = "Product Added Suceesfully!!"
        return render(request,"add.html",{'msg':msg})
    else:    
        return render(request,'add.html')

def view(request):
    seller=User.objects.get(email = request.session['email'])
    product=Product.objects.filter(seller=seller)
    return render(request,'view.html',{'product':product})

def pdetail(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,"product-detail.html",{'product':product})

def pedit(request,pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        product.pcategory = request.POST['pcategory']
        product.price = request.POST['price']
        product.pname = request.POST['pname']
        product.pbrand = request.POST['pbrand']
        product.psize = request.POST['psize']
        product.desc = request.POST['desc']
        try:
            product.ppicture = request.FILES['ppicture']
        except:
            pass
        product.save()
        msg = "Product Updated Sucessfully"
        return render(request,"pedit.html",{'product':product, 'msg':msg})
    else:
        return render(request,"pedit.html",{'product':product})

def pdelete(request,pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect("sindex")

def bpdetail(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,"bpdetail.html",{'product':product})
