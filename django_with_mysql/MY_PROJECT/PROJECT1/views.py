from django.shortcuts import render,redirect
from .models import details,user
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        

        # Check if the username already exists
        if user.objects.filter(username=username).exists():
            messages.error(request, "Username already exists, please choose another one.")
            return render(request, "signup.html")
        
        # Create the user
        user_data=user()
        user_data.username=username
        user_data.password=password
        user_data.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("home")
    
    messages.info(request, "Please fill out the form to create an account.")
    return render(request, "signup.html")



def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        verifyuser=user.objects.filter(username=username,password=password)
        if verifyuser:
            request.session['username']=username
            return redirect("home")
        else:
            return HttpResponse('please enter valid username or password.')
    return render(request,"login.html")


# def signup(request):
#     if request.method=="POST":
#         username=request.POST["username"]
#         password=request.POST["password"]
        # alldata=user.objects.all().values()
        # print(alldata)
        # if user.objects.filter(username=username).exists():
        #     messages.error(request,"Username already exist")
        #     return render(request,"signup.html")
        # else:
        #     new_data=user.objects.create_user(username=username,password=password)
        #     new_data.save()
        #     return redirect("signup")
        
    #     else:
    #         datas=user()
    #         datas.username=username
    #         datas.password=password
    #         datas.save()
    # 
    # return render(request,"signup.html")

# def login(request):

def insert(request):
    if request.method=="POST":
        name=request.POST["name"]
        age=request.POST["age"]
        year_of_joining=request.POST["year_of_joining"]
        depart=request.POST["depart"]
        email=request.POST["mail"]
        data=details()
        data.name=name
        data.age=age
        data.year_of_joining=year_of_joining
        data.depart=depart
        data.email=email
        data.save()
        return redirect("home")
    return render(request,"index.html")
    #    {% url 'insert' %}
# def home(request):

#     data_1=details.objects.all()
#     return render(request,"home.html",{"std":data_1, 'username': request.user.username})

def home(request):
    if 'username' in request.session:
        crt_user=request.session['username']
        user=details.objects.filter(name=crt_user).values()
    return render(request,"home.html",{"std":user})

def edit(request,id):
    data=details.objects.get(id=id)
    if request.method=="POST":
        name=request.POST["name"]
        age=request.POST["age"]
        year_of_joining=request.POST["year_of_joining"]
        depart=request.POST["depart"]
        email=request.POST["mail"]
        data.name=name
        data.age=age
        data.year_of_joining=year_of_joining
        data.depart=depart
        data.email=email
        data.save()
        return redirect("home")
    return render(request,"edit.html",{"data":data,'username': request.user.username})

def delete(request,id):
    data=details.objects.get(id=id)
    data.delete()
    return redirect("home")

def logout(request):
    del request.session['username']
    return redirect("login")

    
