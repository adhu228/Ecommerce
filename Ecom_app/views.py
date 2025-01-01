from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, Payment,OrderPlaced,Wishlist
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@login_required
def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/home.html',locals())


# Category View
@method_decorator(login_required,name='dispatch')
class CategoryViews(View):
    def get(self, request, val):
        totalitem=0
        wishitem=0

        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/category.html', locals())


# Product Details
@method_decorator(login_required,name='dispatch')
class ProductDetails(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product)&Q(user=request.user))
        totalitem=0
        wishitem=0

        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/product_details.html', locals())


# About Page
@login_required
def about(request):
    totalitem=0
    wishitem=0

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/about.html',locals())


# Contact Page
@login_required
def contact(request):
    totalitem=0
    wishitem=0

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/contact.html',locals())


# Customer Registration
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem=0
        wishitem=0

        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congrats! User Registration Successful.")
        else:
            messages.warning(request, "Invalid Input Data.")
        return render(request, 'app/customerregistration.html', locals())


# Profile View
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem=0
        wishitem=0

        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            data = form.cleaned_data
            Customer.objects.create(
                user=user,
                name=data['name'],
                locality=data['locality'],
                city=data['city'],
                mobile=data['mobile'],
                state=data['state'],
                zipcode=data['zipcode'],
            )
            messages.success(request, "Profile saved successfully.")
        else:
            messages.warning(request, "Invalid Input Data.")
        return render(request, 'app/profile.html', locals())


# Address Page
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem=0
    wishitem=0

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/address.html', locals())


# Update Address
@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem=0
        wishitem=0

        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
        else:
            messages.warning(request, "Invalid Input Data.")
        return redirect('address')


# Add to Cart
@login_required
def add_to_cart(request):
    user  =  request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

# Show Cart
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount= amount + value
    totalamount =amount + 40
    totalitem=0
    wishitem=0

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/addtocart.html', locals())

# class checkout(View):
#     def get(self,request):
#         user = request.user
#         add = Customer.objects.filter(user=user)
#         cart_items = Cart.objects.filter(user=user)
#         famount=0
#         for p in cart_items:
#             value = p.quantity * p.product.discounted_price
#             famount = famount + value
#         totalamount = famount + 40
#         return render(request,'app/checkout.html',locals())


@method_decorator(login_required,name='dispatch')
class Checkout(View):
    def get(self, request):
        totalitem=0
        wishitem=0

        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        
        # Handle total amount (including shipping)
        total_amount = sum([item.quantity * item.product.discounted_price for item in cart_items]) + 40
        
        return render(request, 'app/checkout.html', {'total_amount': total_amount, 'addresses': add, 'cart_items': cart_items})

    def post(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        total_amount = sum([item.quantity * item.product.discounted_price for item in cart_items]) + 40
        
        # Payment processing
        payment_method = request.POST.get('payment_method', 'Cash on Delivery')
        payment = Payment.objects.create(
            user=user,
            amount=total_amount,
            paid=True,  # Set this to True once payment is successful
            payment_method=payment_method
        )

        # Optionally: Process the order here and update OrderPlaced model if required.

        messages.success(request, "Payment successful!")
        return redirect('payment_success')  # You can create a success page to notify the user.
    
@login_required
def payment_success(request):
    
    return render(request, 'app/payment_success.html') 



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # Get the cart item for the specified product and user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        # Decrease quantity, but ensure it doesn't go below 1
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        
        # Recalculate the total amount and other details
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40  # Add shipping cost
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        
        return JsonResponse(data)

    
# def remove_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
#         c.delete()
#         user = request.user
#         cart = Cart.objects.filter(user = user)
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount = amount + 40
#         data={
          
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            cart_item.delete()
            # Calculate new cart totals
            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40 if cart.exists() else 0
            return JsonResponse({
                'amount': amount,
                'totalamount': totalamount,
                'cart_empty': not cart.exists()
            })
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
@login_required
def Orders(request):
    totalitem=0
    wishitem=0

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    order_placed = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html', locals())


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added Successfully'
        }
        return JsonResponse(data)
    

def minus_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)  # Ensure the product exists
    wishlist_item = get_object_or_404(Wishlist, user=user, product=product)

    wishlist_item.delete() 
    return redirect('wishlist')  



@login_required
def search(request):
    query = request.GET['search']
    totalitem=0
    wishitem=0

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())


def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()

    return render(request, 'app/wishlist.html', {
        'wishlist_items': wishlist_items,
        'totalitem': totalitem,
        'wishitem': wishitem
    })