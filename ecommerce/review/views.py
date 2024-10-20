# review/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from store.models import Product
from order.models import Order
from .forms import ReviewForm

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_orders = Order.objects.filter(user=request.user, ordered=True, order_items__item=product)
    
    if not user_orders.exists():
        messages.error(request, "You can only review products that you have purchased.")
        return redirect('store:product_detail', slug=product.slug)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.order = user_orders.first()  # Associate the first valid order with the review
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('store:product_detail', slug=product.slug)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'reviews/review_form.html', context)
