# from django.shortcuts import render,redirect
# from django.http import HttpResponseRedirect

# #models
# from payment.models import BillingAddress
# from payment.forms import BillingAddressForm,PaymentMethodForm
# from order.models import Cart,Order

# #view
# from django.views.generic import TemplateView

# # Create your views here.

# class CheckBillingAddressView(TemplateView):
#     template_name = "store/checkout.html"

#     def get(self, request, *args, **kwargs):
#         saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
#         saved_address = saved_address[0]
#         form = BillingAddressForm(instance=saved_address)
#         payment_method = PaymentMethodForm()
#         order_qs = Order.objects.filter(user=request.user, ordered=False)
#         order_item = order_qs[0].order_items.all()
#         order_total = order_qs[0].get_totals()

#         context = {
#             'billing_address':form,
#             'order_item' : order_item,
#             'order_total' : order_total,
#             'payment_method':  payment_method,
#         }
#         return render(request, self.template_name, context=context)
    


#     def post(self, request, *args, **kwargs):

#         saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
#         saved_address = saved_address[0]
#         form = BillingAddressForm(instance=saved_address)
#         payment_obj = Order.objects.filter(user=request.user,ordered=False)[0]
#         payment_form = PaymentMethodForm(instance=payment_obj)
        
#         if request.method == 'post' or request.method == 'POST':
#             form = BillingAddressForm(request.POST,instance=saved_address)
#             pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
#             if form.is_valid() and payment_form.is_valid():
#                 form.save()
#                 pay_method = pay_form.save()
#                 pay_method.save()
#                 return redirect('order:cart')



from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.urls import reverse
from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.conf import settings
from io import BytesIO
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
import logging
import os
from pysslcmz.payment import SSLCSession
from decimal import Decimal
from payment.models import Download

logger = logging.getLogger(__name__)

class CheckBillingAddressView(TemplateView):
    template_name = "store/checkout.html"

    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)[0]
        form = BillingAddressForm(instance=saved_address)
        order_qs = Order.objects.filter(user=request.user, ordered=False).first()
        
        if not order_qs:
            return redirect('order:cart')  # or another page if needed

        order_items = order_qs.order_items.all()
        order_total = order_qs.get_totals()
        payment_method = PaymentMethodForm()
         
        pay_meth = request.GET.get('pay_meth')

        context = {
            'billing_address': form,
            'order_item': order_items,
            'order_total': order_total,
            'payment_method': payment_method,
            'paypal_client_id': settings.PAYPAL_CLIENT_ID,
            'pay_meth': pay_meth ,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
       
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)[0]
        form = BillingAddressForm(request.POST, instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False).first()
        
        if not payment_obj:
           return redirect('order:cart')
        pay_form = PaymentMethodForm(request.POST, instance=payment_obj)


        if form.is_valid() and pay_form.is_valid():
            form.save()
            pay_method = pay_form.save()
            if not saved_address.is_fully_filled():
                print("working")
                return redirect('payment:checkout')  


        
            if pay_method.payment_method == 'Cash on Delivery':
                order_qs = Order.objects.filter(user=request.user, ordered=False)
                order = order_qs[0]
                order.ordered=True
                order.order_id = order.id      
                order.payment_id = pay_method.payment_method
                order.save()
                cart_items = Cart.objects.filter(user=request.user, purchased=False)
                for item in cart_items:
                    item.purchased = True
                    item.save()
                print('order summited successfully')
                return redirect('store:index')
            
            # if pay_method.payment_method == "PayPal":
            #     return redirect(reverse('payment:checkout') + "?pay_meth=" + str(pay_method.payment_method))
            
            #ssl commerce
            if pay_method.payment_method == "SSLcommerz":
                print("hello im ssl")
                store_id = settings.SSL_STORE_ID 
                store_pass = settings.SSL_PASS   
                mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass) 

                status_url = request.build_absolute_uri(reverse('payment:status'))
                mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url) 

                order_qs = Order.objects.filter(user=request.user, ordered=False)
                order_items = order_qs[0].order_items.all()
                order_item_count = order_qs[0].order_items.count()
                order_total = order_qs[0].get_totals()
                mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='clothing', product_name=order_items, num_of_item=order_item_count, shipping_method='Courier', product_profile='None')


                current_user = request.user
                email = current_user.profile.email if current_user.profile.email else "defaultemail@example.com"
                mypayment.set_customer_info(name=current_user.profile.full_name, email=email, address1=current_user.profile.address, address2=current_user.profile.address, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)


                billing_address = BillingAddress.objects.filter(user=request.user)[0]
                mypayment.set_shipping_info(shipping_to=billing_address.address1, address=billing_address.address2, city=billing_address.city, postcode=billing_address.zipcode, country=billing_address.country_name)

                
                response_data = mypayment.init_payment()
                print("==============================")
                print(response_data)
                print("================================")
                return redirect(response_data['GatewayPageURL'])

            return redirect('payment:checkout')

                
        # If forms are not valid, render the page with errors
        context = {
            'billing_address': form,
            'order_item': payment_obj.order_items.all(),
            'order_total': payment_obj.get_totals(),
            'payment_method': pay_form,
        }
        return render(request, self.template_name, context)
    

@csrf_exempt
def sslc_status(request):
    
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        val_id = payment_data['val_id']
        tran_id = payment_data['tran_id']
        print("++++++++++++++++++++++")
        print(payment_data)
        print("+++++++++++++++++++++++++++")
        return HttpResponseRedirect(reverse('payment:sslc_complete',kwargs={'val_id':val_id, 'tran_id':tran_id}))
        
        
    return render(request, 'status.html')

def sslc_complete(request,val_id,tran_id):
    
    Order_qs = Order.objects.filter(user=request.user,ordered=False)
    order=Order_qs[0]
    order.ordered=True
    order.order_id=val_id
    order.payment_id=tran_id
    order.save()
    car_items = Cart.objects.filter(user=request.user,purchased=False)
    for item in car_items:
        item.purchased=True
        item.save()

    #return redirect('store:index')
    return redirect('payment:generate_invoice', order_id=order.order_id)


# def generate_invoice(request, order_id):
#     if not request.user.is_authenticated:
#         return redirect('login')  # Redirect if user is not authenticated

#     # Get the order details
#     order = Order.objects.filter(user=request.user, order_id=order_id).first()
#     if not order:
#         return HttpResponse("Order not found.", status=404)

#     # Create a response object and set the PDF content type
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

#     # Create a PDF object and add content
#     p = canvas.Canvas(response, pagesize=letter)
#     width, height = letter

#     # Invoice Header
#     p.drawString(100, height - 50, "Payment Summary")
#     p.drawString(100, height - 70, f"Invoice number: {order.order_id}")
#     p.drawString(100, height - 90, f"Date: {timezone.now().date()}")
#     p.drawString(100, height - 110, "Please review the following detail for this transaction:")

#     # Amount
#     p.drawString(100, height - 140, f"Amount: {order.get_totals()}")  # Assuming get_totals() returns a formatted amount
#     p.drawString(100, height - 160, f"Description: Products")

#     # Finalize the PDF
#     p.showPage()
#     p.save()
#     return response

# def generate_invoice(request, order_id):
#     if not request.user.is_authenticated:
#         return redirect('login')  # Redirect if user is not authenticated

#     # Get the order details
#     order = get_object_or_404(Order, user=request.user, order_id=order_id)

#     # Create a byte stream buffer to hold the PDF data
#     buffer = BytesIO()

#     # Create a PDF object and add content
#     p = canvas.Canvas(buffer, pagesize=letter)
#     width, height = letter

#     # Invoice Header
#     p.drawString(100, height - 50, "Payment Summary")
#     p.drawString(100, height - 70, f"Invoice number: {order.order_id}")
#     p.drawString(100, height - 90, f"Date: {timezone.now().date()}")
#     p.drawString(100, height - 110, "Please review the following detail for this transaction:")

#     # Amount
#     p.drawString(100, height - 140, f"Amount: {order.get_totals()}")  # Assuming get_totals() returns a formatted amount
#     p.drawString(100, height - 160, "Description: Products")

#     # Finalize the PDF
#     p.showPage()
#     p.save()

#     # Get the PDF from the buffer
#     pdf_data = buffer.getvalue()
#     buffer.close()

#     # Create the path where the file will be saved
#     invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
#     if not os.path.exists(invoice_dir):
#         os.makedirs(invoice_dir)

#     invoice_filename = f"invoice_{order_id}.pdf"
#     invoice_path = os.path.join(invoice_dir, invoice_filename)

#     # Save the PDF file to the invoices directory
#     with open(invoice_path, 'wb') as f:
#         f.write(pdf_data)

#     # Store the download in the user's downloads section
#     user = request.user
#     download = Download.objects.create(user=user, order=order, file=f'invoices/{invoice_filename}')

#     # Send the invoice via email
#     subject = 'Your Invoice from E-shop'
#     message = f"Dear {user.username},\n\nPlease find attached the invoice for your recent order (Order ID: {order.order_id}).\n\nThank you for shopping with us!"
#     email = EmailMessage(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,  # Sender's email address
#         [user.email],  # Recipient's email address
#     )

#     # Attach the PDF file to the email
#     email.attach(invoice_filename, pdf_data, 'application/pdf')

#     # Send the email
#     email.send()

#     # Redirect to the index page after generating the invoice and sending the email
#     return redirect(reverse('store:index'))


def generate_invoice(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect if user is not authenticated

    try:
        # Get the order details
        order = get_object_or_404(Order, user=request.user, order_id=order_id)

        # Create a byte stream buffer to hold the PDF data
        buffer = BytesIO()

        # Create a PDF object and add content
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Invoice Header
        p.drawString(100, height - 50, "Payment Summary")
        p.drawString(100, height - 70, f"Invoice number: {order.order_id}")
        p.drawString(100, height - 90, f"Date: {timezone.now().date()}")
        p.drawString(100, height - 110, "Please review the following detail for this transaction:")

        # Amount
        p.drawString(100, height - 140, f"Amount: {order.get_totals()}")  # Assuming get_totals() returns a formatted amount
        p.drawString(100, height - 160, "Description: Products")

        # Finalize the PDF
        p.showPage()
        p.save()

        # Get the PDF from the buffer
        pdf_data = buffer.getvalue()
        buffer.close()

        # Ensure the 'invoices' directory exists inside 'MEDIA_ROOT'
        invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)  # Create the directory if it doesn't exist

        # Create the path where the file will be saved
        invoice_filename = f"invoice_{order_id}.pdf"
        invoice_path = os.path.join(invoice_dir, invoice_filename)

        # Write the PDF file to the invoices folder
        with open(invoice_path, 'wb') as f:
            f.write(pdf_data)

        # Store the download in the user's downloads section (if applicable)
        user = request.user
        download = Download.objects.create(user=user, order=order, file=f'invoices/{invoice_filename}')

        # Send the invoice via email synchronously
        subject = 'Your Invoice from E-shop'
        message = "Please find attached your invoice."
        email = EmailMessage(subject, message, to=[user.email])
        email.attach(invoice_filename, pdf_data, 'application/pdf')
        email.send()

        logger.info(f"Invoice {order_id} generated and email sent to {user.email}")

    except Exception as e:
        logger.error(f"Error generating invoice for order {order_id}: {e}")
        return HttpResponse("An error occurred while generating the invoice.", status=500)

    # Redirect to the index page after generating the invoice and sending the email
    return redirect(reverse('store:index'))






# def paypalPaymentMethod(request):
#     data = json.loads(request.body)
#     order_id = data['order_id']
#     payment_id = data['payment_id']
#     status = data['status']
#     if status == "COMPLETED":
#         if request.user.is_authenticated:
#                 order_qs = Order.objects.filter(user=request.user, ordered=False)
#                 order = order_qs[0]
#                 order.ordered=True
#                 order.order_id = order_id      
#                 order.payment_id = payment_id
#                 order.save()
#                 cart_items = Cart.objects.filter(user=request.user, purchased=False)
#                 for item in cart_items:
#                     item.purchased = True
#                     item.save()
                
#                 return redirect('store:index')



import json
from django.http import JsonResponse
from django.shortcuts import redirect


def paypalPaymentMethod(request):
    if request.method == "POST":
        try:
           
            data = json.loads(request.body)
            order_id = data.get('order_id')
            payment_id = data.get('payment_id')
            status = data.get('status')
            if not order_id or not payment_id or not status:
                return JsonResponse({'error': 'Missing required payment data.'}, status=400)

            if status == "COMPLETED":
                if request.user.is_authenticated:
                  
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    if order_qs.exists():
                        order = order_qs.first()
                        order.ordered = True
                        order.order_id = order_id
                        order.payment_id = payment_id
                        order.save()

                      
                        cart_items = Cart.objects.filter(user=request.user, purchased=False)
                        for item in cart_items:
                            item.purchased = True
                            item.save()

                        
                        return redirect('store:index')

                    else:
                        return JsonResponse({'error': 'No open order found for this user.'}, status=400)
                else:
                    return JsonResponse({'error': 'User not authenticated.'}, status=401)

           
            return JsonResponse({'error': 'Payment not completed.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
