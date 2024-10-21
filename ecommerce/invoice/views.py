from django.shortcuts import render

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
from .models import Download
from order.models import Order
import os
from django.conf import settings

def generate_invoice(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = Order.objects.filter(user=request.user, order_id=order_id).first()
    if not order:
        return HttpResponse("Order not found.", status=404)

    # Create invoice file path
    invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)
    
    invoice_file = f"invoice_{order_id}.pdf"
    invoice_path = os.path.join(invoice_dir, invoice_file)

    # Generate PDF
    p = canvas.Canvas(invoice_path, pagesize=letter)
    width, height = letter

    # Invoice header
    p.drawString(100, height - 50, "Payment Summary")
    p.drawString(100, height - 70, f"Invoice number: {order.order_id}")
    p.drawString(100, height - 90, f"Date: {timezone.now().date()}")
    p.drawString(100, height - 110, "Transaction details:")

    # Add order details
    y_position = height - 140
    for item in order.order_items.all():
        p.drawString(100, y_position, f"{item.quantity}x {item.item.name} - ${item.get_total()}")
        y_position -= 20

    p.drawString(100, y_position - 20, f"Total: ${order.get_totals()}")

    # Finalize the PDF
    p.showPage()
    p.save()

    # Save the invoice record in Download model
    download = Download(user=request.user, order=order, file=f"invoices/{invoice_file}")
    download.save()

    # Email the invoice to the user
    subject = f"Invoice From E-Shop for Order {order_id}"
    message = f"Dear {request.user.user_name},\n\nPlease find attached the invoice for your order {order_id}."
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])

    # Attach the invoice
    email.attach_file(invoice_path)

    try:
        email.send()
    except Exception as e:
        return HttpResponse(f"Error sending email: {str(e)}", status=500)

    return redirect('store:index')

