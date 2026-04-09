from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from shoppingapp.models import CustomUser,Products, Cart, RegUsers,Order,OrderItem,Tracking,Wishlist,Category,Review, Brand, Subcategory
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.db.models import Count
User = get_user_model()


def BASE(request):    
       return render(request,'base.html')

def BASE1(request):    
       return render(request,'base1.html')

def INDEX(request):
    return render(request,'index.html')


def LOGIN(request):
    return render(request,'login.html')

@login_required(login_url='/')

def DASHBOARD(request):
    brand_count = Brand.objects.all().count()  # Add parentheses
    cat_count = Category.objects.all().count()  # Add parentheses
    subcat_count = Subcategory.objects.all().count()  # Add parentheses
    products_count = Products.objects.all().count()  # Add parentheses
    regusers_count = RegUsers.objects.all().count()  # Add parentheses
    
    newordercount = Order.objects.filter(
        Q(items__status__isnull=True) | Q(items__status='')
    ).count()  # Add parentheses
    
    inprocessordercount = Order.objects.filter(
        Q(items__status='Inprocess')
    ).count()  # Add parentheses
    
    dispatchordercount = Order.objects.filter(
        Q(items__status='Dispatch')
    ).count()  # Add parentheses
    
    deliveredordercount = Order.objects.filter(
        Q(items__status='Delivered')
    ).count()  # Add parentheses

    newrevcount = Review.objects.filter(
        Q(status__isnull=True) | Q(status='') | Q(status=None)
    ).count()  # Add parentheses

    apprevcount = Review.objects.filter(
        Q(status='Approved')
    ).count()  # Add parentheses

    unapprevcount = Review.objects.filter(
        Q(status='Unapproved')
    ).count()  # Add parentheses

    context = {
        'brand_count': brand_count,
        'cat_count': cat_count,
        'subcat_count': subcat_count,
        'products_count': products_count,
        'regusers_count': regusers_count,
        'newordercount': newordercount,
        'inprocessordercount': inprocessordercount,
        'dispatchordercount': dispatchordercount,
        'deliveredordercount': deliveredordercount,
        'newrevcount': newrevcount,
        'apprevcount': apprevcount,
        'unapprevcount': unapprevcount,
    }

    return render(request, 'dashboard.html', context)



def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # This is 'on' if checked, otherwise None
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Set session expiry based on remember_me
            if remember_me:
                # Remember the user for 30 days
                request.session.set_expiry(2592000)  # 30 days in seconds
            else:
                # Browser session: expire when the user closes the browser
                request.session.set_expiry(0)
                
            user_type = user.user_type
            if user_type == '1':
                return redirect('dashboard')
            elif user_type == '2':
                return redirect('index')
        else:
            messages.error(request, 'Email or Password is not valid')
            # Pass the entered username and remember_me back to the template
            return render(request, 'login.html', {'username': username, 'remember_me': remember_me})
    else:
        # If the request method is not POST, redirect to the login page with an error message
        messages.error(request, 'Invalid request method')
        return redirect('login')


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        new_password = request.POST.get('newpassword')

        try:
            user = CustomUser.objects.get(email=email)
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            messages.success(request, "Your password has been successfully changed.")
            return redirect('reset_password')  # Redirect to login page
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email.")

    return render(request, 'reset_password.html')

def doLogout(request):
    logout(request)
    return redirect('login')

def UserLogout(request):
    logout(request)
    return redirect('index')

@login_required(login_url = '/')
def ADMIN_PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)


@login_required(login_url = '/')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('admin_profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'profile.html')

login_required(login_url='/')
def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')



def SHOP(request):
    pro_list = Products.objects.filter(productavailability='In Stock')
    paginator = Paginator(pro_list, 9)  # Show 9 products per page

    page_number = request.GET.get('page')
    try:
        prod = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        prod = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        prod = paginator.page(paginator.num_pages)

    context = {
        'prod': prod,
        'paginator': paginator,
    }
    return render(request, 'shop.html', context)

def SEARCH_PRODUCTS(request):
    query = request.GET.get('query', '')
    
    if query:
        searchprod = Products.objects.filter(
            Q(productname__icontains=query , productavailability='In Stock')  # Using icontains for partial matching
        )

        if searchprod.exists():
            messages.info(request, "Search results for: " + query)
        else:
            messages.info(request, "No records found for: " + query)
        
        # Set up pagination
        paginator = Paginator(searchprod, 10)  # Show 10 results per page
        page = request.GET.get('page')
        
        try:
            searchprod_paginated = paginator.page(page)
        except PageNotAnInteger:
            searchprod_paginated = paginator.page(1)
        except EmptyPage:
            searchprod_paginated = paginator.page(paginator.num_pages)

        return render(request, 'search-products.html', {
            'searchprod': searchprod_paginated,
            'query': query,
        })
    else:
        return render(request, 'search-products.html', {})


def category_detail(request, id):
    catid = get_object_or_404(Category, id=id)
    product_list = Products.objects.filter(cat_id=catid , productavailability='In Stock').order_by('-created_at')
    paginator = Paginator(product_list, 6)  # Show 6 products items per page

    page_number = request.GET.get('page')
    prod = paginator.get_page(page_number)
    
    return render(request, 'categorywise_products.html', {'catid': catid, 'prod': prod})





def VIEWS_PRODUCTS_DETAILS(request, id):
    prod = get_object_or_404(Products, id=id)
    review_list = Review.objects.filter(prod_id=prod, status='Approved')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        # Check if review already exists for this user and product
        existing_review = Review.objects.filter(prod_id=prod, email=request.user.email).first()

        if existing_review:
            messages.warning(request, "You have already submitted a review for this product.")
            return redirect('views_products_details', id=id)

        # Continue creating review if none exists
        review_text = request.POST.get('review', '')
        name = request.user.get_full_name() or request.user.username
        email = request.user.email
        rating = int(request.POST.get('rating', '0'))

        Review.objects.create(
            prod_id=prod,
            review=review_text,
            name=name,
            email=email,
            rating=rating
        )

        messages.success(request, "Your review has been submitted.")
        return redirect('views_products_details', id=id)

    return render(request, 'view_products_details.html', {
        'prod': prod,
        'review_list': review_list,
    })





def THANKYOU(request):
    return render(request, 'thankyou.html')


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Products, id=product_id)
    reguser = get_object_or_404(RegUsers, admin=request.user)
    
    # Handle adding product to cart
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Get the quantity, default to 1 if not found
        
        # Add to cart logic
        cart_item, created = Cart.objects.get_or_create(reguser=reguser, product=product)
        
        if not created:
            cart_item.quantity += quantity  # Update quantity if item already exists in cart
        else:
            cart_item.quantity = quantity  # Set quantity if it's a new item
        
        cart_item.save()
        
        # Remove item from wishlist
        Wishlist.objects.filter(reguser=reguser, product=product).delete()
        
        messages.success(request, f'{product.productname} has been added to your cart.')
        return redirect('view_cart')  # Redirect to the cart page or any other page

    return redirect('product_detail', product_id=product_id)



def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Products, id=product_id)
    reguser = get_object_or_404(RegUsers, admin=request.user)

    # Add the product to the user's wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(reguser=reguser, product=product)

    if created:
        messages.success(request, f'{product.productname} has been added to your wishlist.')
    else:
        messages.info(request, f'{product.productname} is already in your wishlist.')

    return redirect('wishlist_view')  # Redirect to the wishlist page or any other page

@login_required(login_url='/login')
def view_wishlist(request):
    reguser = get_object_or_404(RegUsers, admin=request.user)
    wishlist_items = Wishlist.objects.filter(reguser=reguser).select_related('product')

    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='/login')
def remove_from_wishlist(request, product_id):
    reguser = get_object_or_404(RegUsers, admin=request.user)
    product = get_object_or_404(Products, id=product_id)
    
    # Remove the item from the wishlist
    wishlist_item = Wishlist.objects.filter(reguser=reguser, product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, f'{product.productname} has been removed from your wishlist.')
    else:
        messages.info(request, f'{product.productname} is not in your wishlist.')

    return redirect('wishlist_view')









@login_required(login_url='/login')
def view_cart(request):
    reguser = get_object_or_404(RegUsers, admin=request.user)
    cart_items = Cart.objects.filter(reguser=reguser)
    total = sum([item.get_total_price() for item in cart_items])

    if request.method == 'POST':
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
        transaction_method = request.POST.get('transaction_method')

        if not billing_address or not shipping_address or not transaction_method:
            messages.error(request, "Please fill in all the fields.")
        else:
            # Create the order
            order = Order.objects.create(
                reguser=reguser,
                billing_address=billing_address,
                shipping_address=shipping_address,
                transaction_method=transaction_method
            )

            # Create order items from the cart
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.productprice,
                    shipping_charge=item.product.shippingcharge
                )

            # Clear the cart
            cart_items.delete()

            
            return redirect('order_confirmation')  # Redirect to a confirmation page

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'view_cart.html', context)




@login_required(login_url='/login')
def order_confirmation(request):
    return render(request, 'order-confirmation.html')

@login_required(login_url='/login')
def remove_from_cart(request, cart_id):
    try:
        cart_item = Cart.objects.get(id=cart_id, reguser__admin=request.user)
        cart_item.delete()
        messages.success(request, "Item has been removed from your cart.")
    except Cart.DoesNotExist:
        messages.error(request, "Item not found in your cart.")
    
    return redirect('view_cart')



@login_required(login_url='/login')
def order_history(request):
    reguser = get_object_or_404(RegUsers, admin=request.user)
    orders = Order.objects.filter(reguser=reguser).prefetch_related('items__product')

    # Calculate the total price for each order
    order_totals = []
    for order in orders:
        total_price = sum([item.get_total_item_price() for item in order.items.all()])
        order_totals.append((order, total_price))

    # Set up pagination with 5 orders per page (you can adjust this)
    paginator = Paginator(order_totals, 5)  # 5 orders per page
    page = request.GET.get('page', 1)

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)  # If page is not an integer, deliver the first page
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page

    context = {
        'order_totals': paginated_orders,
    }
    return render(request, 'order_history.html', context)


@login_required(login_url='/login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, reguser__admin=request.user)
    order_items = order.items.all()

    total_price = sum([item.get_total_item_price() for item in order_items])

    # Determine if all items are cancelable
    cancelable = all(item.status in ['', None, 'Inprocess'] for item in order_items)

    # Determine if all items are cancelled
    all_cancelled = all(item.status == 'Cancel' for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'cancelable': cancelable,
        'all_cancelled': all_cancelled,
    }
    return render(request, 'order_detail.html', context)

@login_required(login_url='/login')
def cancel_order(request, order_id):
    # Ensure that the user is the owner of the order
    order = get_object_or_404(Order, id=order_id, reguser__admin=request.user)
    
    # Fetch all order items
    order_items = order.items.all()
    
    # Check if items can still be canceled (status is 'Inprocess', '' or None)
    cancelable_items = [item for item in order_items if item.status in ['Inprocess', '', None]]
    
    if cancelable_items:
        # Update the status of cancelable items
        for item in cancelable_items:
            item.status = 'Cancel'
            item.save()
        
        # Optionally, create a tracking record for the cancellation
        Tracking.objects.create(
            order=order,
            remark="Order Cancelled",
            status="Cancel"
        )

        messages.success(request, "Order has been cancelled successfully.")
    else:
        # If none of the items are cancelable, show an error message
        messages.error(request, "The order cannot be cancelled as it has been dispatched or delivered.")

    return redirect('order_detail', order_id=order_id)

@login_required(login_url='/login')
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, reguser__admin=request.user)
    tracking_info = Tracking.objects.filter(order=order).order_by('updated_at')

    context = {
        'order': order,
        'tracking_info': tracking_info,
    }
    return render(request, 'track_order.html', context)



@login_required(login_url='/login')
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, reguser__admin=request.user)
    order_items = order.items.all()

    # Check if the order is canceled by checking if all items are canceled
    if all(item.status == 'Cancel' for item in order_items):
        messages.error(request, "Invoice cannot be generated because the order is canceled.")
        return redirect('order_detail', order_id=order_id)  # Redirect to a different view, e.g., order history or order detail

    total_price = sum([item.get_total_item_price() for item in order_items])

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
    }

    return render(request, 'invoice.html', context)

def ABOUTUS(request):
    return render(request, 'aboutus.html')

