from django.shortcuts import render,redirect
from account.forms import RegistrationForm
from django.http import HttpResponse

#authentication function
from django.contrib.auth import authenticate,login,logout
from order.models import Cart, Order
from payment.models import BillingAddress
from account.models import Profile
from payment.forms import BillingAddressForm

from django.views.generic import TemplateView

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


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
       orders = Order.objects.filter(user=request.user, ordered = True)
       billingaddress = BillingAddress.objects.get(user=request.user)
       billingaddress_form = BillingAddressForm(instance=billingaddress)
       context = {
           
          'orders' : orders,
           'billingaddress': billingaddress_form ,

       }

       return render(request,'profile.html',context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method == 'post':
             billingaddress = BillingAddress.objects.get(user=request.user)

             billingaddress_form = BillingAddressForm(request.POST,instance=billingaddress)
            
             if billingaddress_form.is_valid():
                billingaddress_form.save()
                return redirect('account:profile')

               
             