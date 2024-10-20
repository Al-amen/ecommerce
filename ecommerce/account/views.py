from django.shortcuts import render,redirect
from account.forms import RegistrationForm,ProfileForm
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
                  user = form.save(commit=False)
                  user.is_active = True 
                  user.save()
                  return HttpResponse("your account has been created")
     

        context = {
         'form': form
       }


    return render(request, 'register.html', context=context)


def Customerlogin(request):
    
    if request.user.is_authenticated:
        return HttpResponse("You are already logged in")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Login attempt with username: {username} and password: {password}")

        # Authenticate using the custom backend
        customer = authenticate(request, username=username, password=password)

        if customer is None:
            print(f"Failed to authenticate user: {username}")
        else:
            print(f"User {customer} authenticated successfully")

        if customer is not None:
            if customer.is_active:
                login(request, customer)
                return  redirect('store:index')
            else:
                return HttpResponse("User is inactive or not verified.")
        else:
            return HttpResponse("Invalid username or password.")

    # Handle GET requests or any other method
    return render(request, 'login.html')



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('store:index')
    else:
        return redirect("account:login")
    


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
       orders = Order.objects.filter(user=request.user, ordered = True)
       billingaddress = BillingAddress.objects.get(user=request.user)
       billingaddress_form = BillingAddressForm(instance=billingaddress)
       profile_obj = Profile.objects.get(user=request.user)
       profileForm = ProfileForm(instance=profile_obj)
       context = {
           
          'orders' : orders,
           'billingaddress': billingaddress_form ,
           'profileForm':profileForm ,

       }

       return render(request,'profile.html',context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method == 'post':
             billingaddress = BillingAddress.objects.get(user=request.user)
             billingaddress_form = BillingAddressForm(request.POST,instance=billingaddress)

             profile_obj = Profile.objects.get(user=request.user)
             profileForm = ProfileForm(request.POST,instance=profile_obj)

             if billingaddress_form.is_valid() or profileForm.is_valid():
                billingaddress_form.save()
                profileForm.save()
                return redirect('account:profile')

               
             