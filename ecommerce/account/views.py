from django.shortcuts import render
from account.forms import RegistrationForm
from django.http import HttpResponse

#authentication function
from django.contrib.auth import authenticate,login,logout

def register(request):
    
    if request.user.is_authenticated:
        return HttpResponse("Your are already authentiacted")
    else:
        form = RegistrationForm()
        if request.method == "post" or request.method == "POST":
             form = RegistrationForm(request.POST)
             if form.is_valid():
                 form.save()
                 return HttpResponse("your account has been created")
     

        context = {
         'form': form
       }


    return render(request, 'register.html', context=context)


def Customerlogin(request):
    
    if request.user.is_authenticated:
        return HttpResponse("you are already logined")
    
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request,username=username,password=password)
            print(username)
            print(password)
            print(customer)
            if customer is not None:
                login(request,customer)
                return HttpResponse("sucessfully logined!")
            else:
                return HttpResponse("404")
    
    return render(request, 'login.html')

