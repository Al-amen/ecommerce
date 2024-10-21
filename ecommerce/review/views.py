# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Review,ReviewImage
# from store.models import Product
# from order.models import Order
# from .forms import ReviewForm

# @login_required
# def submit_review(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     user_orders = Order.objects.filter(user=request.user, ordered=True, order_items__item=product)

#     # Ensure the user has purchased the product before allowing review submission
#     if not user_orders.exists():
#         messages.error(request, "You can only review products that you have purchased.")
#         return redirect('store:product_detail', slug=product.slug)

#     if request.method == "POST":
#         form = ReviewForm(request.POST, request.FILES)  # include request.FILES for handling images
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.product = product
#             review.order = user_orders.first()  # Associate the first valid order with the review
#             review.save()

#             # Handle image uploads
#             images = request.FILES.getlist('images')
#             for image in images:
#                 ReviewImage.objects.create(review=review, image=image)

#             messages.success(request, "Thank you for your review!")
#             return redirect('store:product_detail', slug=product.slug)
#     else:
#         form = ReviewForm()

#     context = {
#         'form': form,
#         'product': product,
#     }
#     return render(request, 'reviews/review_form.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, ReviewImage
from store.models import Product
from order.models import Order
from .forms import ReviewForm

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_orders = Order.objects.filter(user=request.user, ordered=True, order_items__item=product)

    # Check if the user has already reviewed this product
    review = Review.objects.filter(user=request.user, product=product).first()

    if request.method == "POST":
        if review:
            form = ReviewForm(request.POST, request.FILES, instance=review)  # Edit existing review
        else:
            form = ReviewForm(request.POST, request.FILES)  # Create new review

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.order = user_orders.first()  # Associate the first valid order with the review
            review.save()

            # Handle image uploads
            images = request.FILES.getlist('images')
            for image in images:
                ReviewImage.objects.create(review=review, image=image)

            messages.success(request, "Thank you for your review!")
            return redirect('store:product_detail', slug=product.slug)
    else:
        form = ReviewForm(instance=review)  # Pass the existing review instance if it exists

    context = {
        'form': form,
        'product': product,
        'review': review,  # Pass the review object to the template
    }
    return render(request, 'reviews/review_form.html', context)

# @login_required
# def delete_review(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     review = get_object_or_404(Review, user=request.user, product=product)

#     if request.method == "POST":
#         review.delete()
#         messages.success(request, "Your review has been deleted.")
#         return redirect('store:product_detail', slug=product.slug)

#     context = {
#         'product': product,
#         'review': review,
#     }
#     return render(request, 'reviews/delete_review_confirm.html', context)


@login_required
def delete_review(request, product_id):
    review = get_object_or_404(Review, product_id=product_id, user=request.user)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('store:product_detail', slug=review.product.slug)

    return redirect('store:product_detail', slug=review.product.slug)