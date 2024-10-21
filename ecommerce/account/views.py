from django.contrib import messages
from django.shortcuts import render,redirect
from account.forms import RegistrationForm,ProfileForm
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
#authentication function
from django.contrib.auth import authenticate,login,logout
from order.models import Cart, Order
from payment.models import BillingAddress
from account.models import Profile,Verification
from payment.forms import BillingAddressForm
from django.views.generic import TemplateView

import uuid



def send_email_after_registration(email, token):
    subject = "Verify Email"
    message = f"""
    Dear Sir/Madam,

    ATTN: Please do not reply to this email. This mailbox is not monitored, and you will not receive a response.

    Your Verification Email is given below 👇
    Click on the link to verify your account http://127.0.0.1:8000/account/account-verify/{token}

    If you have any queries, please contact us at:

    E-SHOP,
    Kirtipur, Kathmandu, Nepal.
    Phone: 01650141474
    Email: abc@gmail.com

    Warm Regards,
    E-shop
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)


def register(request):
    
    if request.user.is_authenticated:
        messages.info(request,"You are already logined!")
        return redirect('store:index')
        
    else:
        form = RegistrationForm()
        
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.is_active = False  # Account is inactive until verified
                new_user.save()

                # Generate token and send verification email
                uid = uuid.uuid4()
                Verification.objects.create(user=new_user, token=uid)
                send_email_after_registration(new_user.email, uid)

                messages.success(request, "Your account has been created. Please check your email for verification.")
               
     
        context = {
            'form': form,
            
        }
        return render(request, 'register.html', context=context)


def account_verify(request, token):
    
    pf = Verification.objects.filter(token=token).first()
    print(f"Verification object: {pf}")
    if pf:
        pf.verify = True
        pf.save()
        pf.user.is_active = True  # Activate user after verification
        pf.user.save()
        messages.success(request, "Your account has been verified. You can log in now.")
        print("Your account has been verified. You can log in now.")
        return redirect('account:login')
    else:
        messages.error(request, "Invalid verification token.")
        print("Invalid verification token.")
        return redirect('account:login')

def Customerlogin(request):
    
    if request.user.is_authenticated:
        messages.info(request,"You are already logged in")
        return redirect('store:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate using the provided credentials
        customer = authenticate(request, username=username, password=password)

        if customer is not None:
            pro = Verification.objects.get(user=customer)
            if pro.verify:  # Check if the account is verified
                login(request, customer)
                return redirect('store:index')
            else:
                messages.info(request, 'Your account is not verified. Please check your email to verify your account.')
                print("Your account is not verified. Please check your email to verify your account.")
                return redirect('/account/login/')
        else:
            messages.error(request, "Invalid username or password.")
            print("Invalid username or password.")
    
    return render(request, 'login.html')





# def register(request):
    
#     if request.user.is_authenticated:
#         return HttpResponse("Your are already authentiacted")
#     else:
#         form = RegistrationForm()
#         if request.method == "post" or request.method == "POST":
#              form = RegistrationForm(request.POST)
#              if form.is_valid():
#                   user = form.save(commit=False)
#                   user.is_active = True 
#                   user.save()
#                   return HttpResponse("your account has been created")
     

#         context = {
#          'form': form
#        }


#     return render(request, 'register.html', context=context)


# def Customerlogin(request):
    
#     if request.user.is_authenticated:
#         return HttpResponse("You are already logged in")

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         print(f"Login attempt with username: {username} and password: {password}")

#         # Authenticate using the custom backend
#         customer = authenticate(request, username=username, password=password)

#         if customer is None:
#             print(f"Failed to authenticate user: {username}")
#         else:
#             print(f"User {customer} authenticated successfully")

#         if customer is not None:
#             if customer.is_active:
#                 login(request, customer)
#                 return  redirect('store:index')
#             else:
#                 return HttpResponse("User is inactive or not verified.")
#         else:
#             return HttpResponse("Invalid username or password.")

#     # Handle GET requests or any other method
#     return render(request, 'login.html')



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('store:index')
    else:
        return redirect("account:login")
    


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
       orders = Order.objects.filter(user=request.user, ordered = True).order_by('-created')
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

               
             