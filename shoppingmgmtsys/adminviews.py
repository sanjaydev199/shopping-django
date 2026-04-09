from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from shoppingapp.models import CustomUser, Brand, Category, Subcategory, Products,Order,OrderItem,Tracking,Review,RegUsers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Sum
from django.utils.dateparse import parse_date
User = get_user_model()

@login_required(login_url='/')
def ADD_BRAND(request):
    if request.method == "POST":
        brandname = request.POST.get('brandname')
        brandlogo = request.FILES.get('brandlogo')
        brands =Brand(
            brandname=brandname,
            brandlogo=brandlogo,
        )
        brands.save()
        messages.success(request,'Brands has been added succeesfully!!!')
        return redirect("add_brand")    
    return render(request,'admin/add-brand.html')


@login_required(login_url='/')
def MANAGE_BRAND(request):
    
    brand_list = Brand.objects.all()
    paginator = Paginator(brand_list, 10)  # Show 10 brands per page

    page_number = request.GET.get('page')
    try:
        brands = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        brands = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        brands = paginator.page(paginator.num_pages)

    context = {'brands': brands,
    }
    return render(request, 'admin/manage-brand.html', context)


@login_required(login_url='/')
def DELETE_BRAND(request,id):
    brands = Brand.objects.get(id=id)
    brands.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    return redirect('manage_brand')



login_required(login_url='/')
def UPDATE_BRAND(request,id):
    brand = Brand.objects.get(id=id)
    
    context = {
         'brand':brand,
        
    }

    return render(request,'admin/update_brand.html',context)


@login_required(login_url='/')
def UPDATE_BRAND_DETAILS(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        brandname = request.POST.get('brandname')
        brandlogo = request.FILES.get('brandlogo')  # Get the uploaded file, if any

        # Retrieve the brand object using the provided id
        brand = Brand.objects.get(id=bid)

        # Update the brand name
        brand.brandname = brandname

        # Only update the logo if a new one is uploaded
        if brandlogo:
            brand.brandlogo = brandlogo

        # Save the updated brand details
        brand.save()

        # Display a success message
        messages.success(request, "Your brand details have been updated successfully")
        
        # Redirect to the manage brands page (or any other page)
        return redirect('manage_brand')

    # If the request method is not POST, just render the form (this might not be necessary for your use case)
    return render(request, 'admin/update_brand.html')


@login_required(login_url='/')
def ADD_CATEGORY(request):
    if request.method == "POST":
        catname = request.POST.get('catname')
        catdes = request.POST.get('catdes')
        cat =Category(
            catname=catname,
            catdes=catdes,
        )
        cat.save()
        messages.success(request,'Category has been added succeesfully!!!')
        return redirect("add_category")
    
    return render(request,'admin/add-category.html')

@login_required(login_url='/')
def MANAGE_CATEGORY(request):
    
    cat_list = Category.objects.all()
    paginator = Paginator(cat_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)

    context = {'categories': categories,
    }
    return render(request, 'admin/manage-category.html', context)

@login_required(login_url='/')
def DELETE_CATEGORY(request,id):
    cat = Category.objects.get(id=id)
    cat.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_category')

login_required(login_url='/')
def UPDATE_CATEGORY(request,id):
    category = Category.objects.get(id=id)
    
    context = {
         'category':category,
        
    }

    return render(request,'admin/update_category.html',context)

login_required(login_url='/')

def UPDATE_CATEGORY_DETAILS(request):
        if request.method == 'POST':
          cat_id = request.POST.get('cat_id')
          catname = request.POST.get('catname')
          catdes = request.POST.get('catdes')
          category = Category.objects.get(id=cat_id) 
          category.catname = catname
          category.catdes = catdes
          category.save()   
          messages.success(request,"Your category detail has been updated successfully")
          return redirect('manage_category')
        return render(request, 'admin/update_category.html')

@login_required(login_url = '/')
def ADD_SUBCATEGORY(request):    
    category = Category.objects.all()
    if request.method == "POST":
        cat_id = request.POST.get('cat_id')
        subcatname = request.POST.get('subcatname')
        cid = Category.objects.get(id=cat_id)
        Subcat = Subcategory(cat_id=cid, subcatname = subcatname,
        )
        Subcat.save()
        messages.success(request, 'Subcategory Added Succeesfully!!!')
        return redirect("add_subcategory")
    context = {
        'category':category,
        
    }
    return render(request,'admin/add_subcategory.html',context)


def MANAGE_SUBCATEGORY(request):
    subcategory_list = Subcategory.objects.all()
    paginator = Paginator(subcategory_list, 10)  # Show 10 subcategories per page

    page_number = request.GET.get('page')
    try:
        subcategories = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        subcategories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        subcategories = paginator.page(paginator.num_pages)

    context = {'subcategories': subcategories,
     }
    return render(request, 'admin/manage_subcategory.html', context)

@login_required(login_url='/')
def DELETE_SUBCATEGORY(request,id):
    subcategory = Subcategory.objects.get(id=id)
    subcategory.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_subcategory')


login_required(login_url='/')
def UPDATE_SUBCATEGORY(request,id):
    
    category = Category.objects.all()
    subcategory = Subcategory.objects.get(id=id)
    
    context = {
         'subcategory':subcategory,
         'category':category,
        
    }

    return render(request,'admin/update_subcategory.html',context)


login_required(login_url='/')

def UPDATE_SUBCATEGORY_DETAILS(request):
        if request.method == 'POST':
          subcat_id = request.POST.get('subcat_id')
          cat_id = request.POST.get('cat_id')
          subcatname = request.POST.get('subcatname')
          subcategory = Subcategory.objects.get(id=subcat_id) 
          categoryid = Category.objects.get(id=cat_id) 
          subcategory.cat_id = categoryid
          subcategory.subcatname = subcatname
          subcategory.save()   
          messages.success(request,"Your subcategory detail has been updated successfully")
          return redirect('manage_subcategory')
        return render(request, 'admin/update_subcategory.html')



@login_required(login_url='/')

def get_subcat(request):
    if request.method == 'GET':
        c_id = request.GET.get('c_id')
        subcat = Subcategory.objects.filter(cat_id=c_id)
        subcat_options = ''
        for subcategory in subcat:
            subcat_options += f'<option value="{subcategory.id}">{subcategory.subcatname}</option>'
        return JsonResponse({'subcat_options': subcat_options})

login_required(login_url='/')
def ADD_PRODUCTS(request):

    category = Category.objects.all()
    brands = Brand.objects.all()
    if request.method == "POST":
        cat_id = request.POST.get('cat_id')
        subcategory_id_value = request.POST.get('subcategory_id')  
        productname = request.POST.get('productname')
        brand_id = request.POST.get('brand_id')
        productpricebd = request.POST.get('productpricebd')
        productprice = request.POST.get('productprice')
        description = request.POST.get('description')
        shippingcharge = request.POST.get('shippingcharge')
        productavailability = request.POST.get('productavailability')
        productimage1 = request.FILES.get('productimage1')
        productimage2 = request.FILES.get('productimage2')
        productimage3 = request.FILES.get('productimage3')

        cid = Category.objects.get(id=cat_id)
        subcategory_id = Subcategory.objects.get(id=subcategory_id_value)
        bid = Brand.objects.get(id=brand_id)

        products = Products(cat_id=cid,
            subcategory_id=subcategory_id,
            productname = productname,
            brand_id = bid,
            description = description,
            productpricebd = productpricebd,
            productprice = productprice,
            shippingcharge = shippingcharge,
            productavailability = productavailability,
            productimage1 = productimage1,
            productimage2 = productimage2,
            productimage3 = productimage3,
            )
        products.save()
        messages.success(request, 'Product added Successfully!!!')
        return redirect("add_products")

    context = {
        'category': category,
        'brands':brands,
       
    }    

    return render(request, 'admin/add-products.html', context)

def MANAGE_PRODUCTS(request):
    pro_list = Products.objects.all()
    paginator = Paginator(pro_list, 10)  # Show 10 subcategories per page

    page_number = request.GET.get('page')
    try:
        prod = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        prod = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        prod = paginator.page(paginator.num_pages)

    context = {'prod': prod,
     }
    return render(request, 'admin/manage_products.html', context)

@login_required(login_url='/')
def DELETE_PRODUCTS(request,id):
    prod = Products.objects.get(id=id)
    prod.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    return redirect('manage_products')

login_required(login_url='/')
def VIEWS_PRODUCTS(request,id):   
    prod = Products.objects.get(id=id)    
    context = {
          'prod':prod,
          'categories': Category.objects.all(),
          'subcategories': Subcategory.objects.all(),
           'brands': Brand.objects.all(),   
        
    }
    return render(request,'admin/update_products.html',context)

@login_required(login_url='/')
def UPDATE_PRODUCTS(request):
    if request.method == 'POST':
        # Fetch form data
        pro_id = request.POST.get('pro_id')
        subcat_id = request.POST.get('subcat_id')
        cat_id = request.POST.get('cat_id')
        productname = request.POST.get('productname')
        brand_id = request.POST.get('brand_id')
        productpricebd = request.POST.get('productpricebd')
        productprice = request.POST.get('productprice')
        description = request.POST.get('description')
        shippingcharge = request.POST.get('shippingcharge')
        productavailability = request.POST.get('productavailability')

        # Fetch uploaded images (if any)
        productimage1 = request.FILES.get('productimage1')
        productimage2 = request.FILES.get('productimage2')
        productimage3 = request.FILES.get('productimage3')

        try:
            # Get the product, category, subcategory, and brand
            prod = get_object_or_404(Products, id=pro_id)
            subcategory = get_object_or_404(Subcategory, id=subcat_id)
            category = get_object_or_404(Category, id=cat_id)
            brand = get_object_or_404(Brand, id=brand_id)

            # Update product fields
            prod.cat_id = category
            prod.subcategory_id = subcategory
            prod.brand_id = brand
            prod.productname = productname
            prod.productpricebd = productpricebd
            prod.productprice = productprice
            prod.description = description
            prod.shippingcharge = shippingcharge
            prod.productavailability = productavailability

            # Update images only if new ones are uploaded
            if productimage1:
                prod.productimage1 = productimage1
            if productimage2:
                prod.productimage2 = productimage2
            if productimage3:
                prod.productimage3 = productimage3

            # Save the updated product details
            prod.save()

            # Success message
            messages.success(request, "Your product details have been updated successfully")
            return redirect('manage_products')

        except (Subcategory.DoesNotExist, Category.DoesNotExist, Brand.DoesNotExist):
            messages.error(request, "Invalid subcategory, category, or brand ID provided.")
            return redirect('views_products')

    else:
        # If GET request, render the product update form with the current product details
        pro_id = request.GET.get('pro_id')
        prod = get_object_or_404(Products, id=pro_id)
        context = {
            'prod': prod,
           
        }
        return render(request, 'admin/update_products.html', context)





@login_required(login_url='/')
def NEWORDER(request):
    # Fetch orders with OrderItems and related Products
    orders = Order.objects.filter(
    Q(items__status__isnull=True) | Q(items__status='')
).prefetch_related('items__product').distinct()

    # Calculate total price for each order
    order_totals = [(order, sum([item.get_total_item_price() for item in order.items.all()])) for order in orders]

    # Paginate the orders
    page = request.GET.get('page', 1)
    paginator = Paginator(order_totals, 10)  # Show 10 orders per page

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    # Pass the paginated orders to the context
    context = {
        'paginated_orders': paginated_orders,
    }

    return render(request, 'admin/new-order.html', context)

@login_required(login_url='/')
def INPROCESSORDER(request):
    # Fetch orders with OrderItems and related Products
    orders = Order.objects.filter(
   Q(items__status='Inprocess')
).prefetch_related('items__product').distinct()

    # Calculate total price for each order
    order_totals = [(order, sum([item.get_total_item_price() for item in order.items.all()])) for order in orders]

    # Paginate the orders
    page = request.GET.get('page', 1)
    paginator = Paginator(order_totals, 10)  # Show 10 orders per page

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    # Pass the paginated orders to the context
    context = {
        'paginated_orders': paginated_orders,
    }

    return render(request, 'admin/inprocess-order.html', context)


@login_required(login_url='/')
def DISPATCHORDER(request):
    # Fetch orders with OrderItems and related Products
    orders = Order.objects.filter(
   Q(items__status='Dispatch')
).prefetch_related('items__product').distinct()

    # Calculate total price for each order
    order_totals = [(order, sum([item.get_total_item_price() for item in order.items.all()])) for order in orders]

    # Paginate the orders
    page = request.GET.get('page', 1)
    paginator = Paginator(order_totals, 10)  # Show 10 orders per page

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    # Pass the paginated orders to the context
    context = {
        'paginated_orders': paginated_orders,
    }

    return render(request, 'admin/dispatch-order.html', context)

@login_required(login_url='/')
def DELIVEREDORDER(request):
    # Fetch orders with OrderItems and related Products
    orders = Order.objects.filter(
   Q(items__status='Delivered')
).prefetch_related('items__product').distinct()

    # Calculate total price for each order
    order_totals = [(order, sum([item.get_total_item_price() for item in order.items.all()])) for order in orders]

    # Paginate the orders
    page = request.GET.get('page', 1)
    paginator = Paginator(order_totals, 10)  # Show 10 orders per page

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    # Pass the paginated orders to the context
    context = {
        'paginated_orders': paginated_orders,
    }

    return render(request, 'admin/delivered-order.html', context)

@login_required(login_url='/')
def CANCELEDORDER(request):
    # Fetch orders with OrderItems and related Products
    orders = Order.objects.filter(
   Q(items__status='Cancel')
).prefetch_related('items__product').distinct()

    # Calculate total price for each order
    order_totals = [(order, sum([item.get_total_item_price() for item in order.items.all()])) for order in orders]

    # Paginate the orders
    page = request.GET.get('page', 1)
    paginator = Paginator(order_totals, 10)  # Show 10 orders per page

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    # Pass the paginated orders to the context
    context = {
        'paginated_orders': paginated_orders,
    }

    return render(request, 'admin/cancel-order.html', context)

@login_required(login_url='/')
def ALLORDER(request):
    # Fetch orders with OrderItems and related Products
    orders = Order.objects.all(
   
).prefetch_related('items__product').distinct()

    # Calculate total price for each order
    order_totals = [(order, sum([item.get_total_item_price() for item in order.items.all()])) for order in orders]

    # Paginate the orders
    page = request.GET.get('page', 1)
    paginator = Paginator(order_totals, 10)  # Show 10 orders per page

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    # Pass the paginated orders to the context
    context = {
        'paginated_orders': paginated_orders,
    }

    return render(request, 'admin/all-order.html', context)


@login_required(login_url='/login')
def view_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    total_price = sum([item.get_total_item_price() for item in order_items])
    tracking_history = Tracking.objects.filter(order=order).order_by('updated_at')

    # Check if any OrderItem has a status of '' or '0'
    has_pending_items = any(item.status in ['', '0', 'Inprocess','Dispatch'] for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'has_pending_items': has_pending_items,
        'tracking_history': tracking_history,
    }
    return render(request, 'admin/view_order_detail.html', context)

@login_required(login_url='/')
def update_order(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        remark = request.POST.get('remark')
        status = request.POST.get('status')
        
        # Update all OrderItems in the order if their status is '' or '0'
        for item in order.items.all():
            if item.status in ['', '0', 'Inprocess','Dispatch']:
                item.status = status
                item.remark = remark
                item.save()

        # Create a new tracking record
        Tracking.objects.create(
            order=order,
            remark=remark,
            status=status
        )
        
        messages.success(request, "Status updated successfully")
        return redirect('view_order_detail', order_id=id)

    tracking_history = Tracking.objects.filter(order=order).order_by('updated_at')

    context = {
        'order': order,
        'tracking_history': tracking_history,
    }
    return render(request, 'admin/view_order_detail.html', context)


@login_required(login_url='/')
def Search_Order(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter by order id, mobilenumber, or user's first or last name
            order_search = Order.objects.filter(
                Q(id__icontains=query) |
                Q(reguser__mobilenumber__icontains=query) |
                Q(reguser__admin__first_name__icontains=query) |
                Q(reguser__admin__last_name__icontains=query)
            )

            if order_search.exists():
                messages.success(request, f"Search results for '{query}'")
            else:
                messages.warning(request, f"No records found for '{query}'")
            
            # Paginate the results
            paginator = Paginator(order_search, 10)  # Show 10 orders per page
            page_number = request.GET.get('page', 1)
            try:
                paginated_orders = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_orders = paginator.page(1)
            except EmptyPage:
                paginated_orders = paginator.page(paginator.num_pages)

            return render(request, 'admin/search-order.html', {
                'order_search': paginated_orders, 
                'query': query,
                'paginated_orders': paginated_orders
            })
        else:
            
            return render(request, 'admin/search-order.html', {})

@login_required(login_url='/')
def Between_Date_Order_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    orders = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'admin/betdates-order-report.html', {'orders': orders, 'error_message': 'Invalid date format'})

        # Filter orders between the given date range
        orders = Order.objects.filter(created_at__range=(start_date, end_date))

    return render(request, 'admin/betdates-order-report.html', {'orders': orders, 'start_date': start_date, 'end_date': end_date})





@login_required(login_url='/')
def sales_report(request):
    if request.method == 'POST':
        # Get the start and end dates from the form
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parse the dates
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if start_date and end_date:
            # Filter orders between the selected dates and items with status 'Delivered'
            orders = Order.objects.filter(
                created_at__date__gte=start_date,
                created_at__date__lte=end_date,
                items__status='Delivered'
            ).distinct()  # Use distinct to avoid duplicates when filtering related models

            # Create a list to store order details and calculate per-order totals
            order_data = []
            for order in orders:
                total_quantity = order.items.aggregate(Sum('quantity'))['quantity__sum'] or 0
                total_price = order.items.aggregate(Sum('price'))['price__sum'] or 0
                total_shipping = order.items.aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0

                order_data.append({
                    'order': order,
                    'total_quantity': total_quantity,
                    'total_price': total_price,
                    'total_shipping': total_shipping,
                })
            
            # Calculate overall totals
            overall_quantity = sum([data['total_quantity'] for data in order_data])
            overall_price = sum([data['total_price'] for data in order_data])
            overall_shipping = sum([data['total_shipping'] for data in order_data])
            
            return render(request, 'admin/sales_report.html', {
                'order_data': order_data,
                'overall_quantity': overall_quantity,
                'overall_price': overall_price,
                'overall_shipping': overall_shipping,
                'start_date': start_date,
                'end_date': end_date
            })
        else:
            messages.error(request, "Please provide both start and end dates.")
    
    return render(request, 'admin/sales_report.html')


@login_required(login_url='/')
def Registered_Users(request):
    regusers_list = RegUsers.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(regusers_list, 10)  # Show 10 regusers per page

    try:
        regusers = paginator.page(page)
    except PageNotAnInteger:
        regusers = paginator.page(1)
    except EmptyPage:
        regusers = paginator.page(paginator.num_pages)

    context = {'regusers': regusers}
    return render(request, 'admin/reguser.html', context)

@login_required(login_url='/')
def DELETE_REGUSERS(request, id):
    try:
        reguser = get_object_or_404(RegUsers, id=id)
        custom_user = reguser.admin  # Access the related CustomUser
        reguser.delete()  # This will also delete the associated CustomUser because of the on_delete=models.CASCADE
        custom_user.delete()
        messages.success(request, 'Record deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting record: {e}')
    return redirect('registered_users')

login_required(login_url='/')
def REGUSERS_ORDERS(request,id):
    order_list = Order.objects.filter(reguser=id)
    
    context = {
         'order_list':order_list,
    }

    return render(request,'admin/regusers-order-details.html',context)


@login_required(login_url='/')
def ALLREVIEWS(request):    
    all_rev = Review.objects.all()
    paginator = Paginator(all_rev, 10)  # Show 10 enquiries per page

    page_number = request.GET.get('page')
    try:
        all_rev = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_rev = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_rev = paginator.page(paginator.num_pages)

    context = {
        'all_rev': all_rev,
    }
    return render(request, 'admin/all_reviews.html', context)

@login_required(login_url='/')
def NEWREVIEWS(request):    
    approved_rev = Review.objects.filter(Q(status__isnull=True) | Q(status='') | Q(status=None))
    paginator = Paginator(approved_rev, 10)  # Show 10 enquiries per page

    page_number = request.GET.get('page')
    try:
        approved_rev = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        approved_rev = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        approved_rev = paginator.page(paginator.num_pages)

    context = {
        'approved_rev': approved_rev,
    }
    return render(request, 'admin/new_reviews.html', context)
@login_required(login_url='/')
def APPROVEDREVIEWS(request):    
    approved_rev = Review.objects.filter( Q(status='Approved'))
    paginator = Paginator(approved_rev, 10)  # Show 10 enquiries per page

    page_number = request.GET.get('page')
    try:
        approved_rev = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        approved_rev = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        approved_rev = paginator.page(paginator.num_pages)

    context = {
        'approved_rev': approved_rev,
    }
    return render(request, 'admin/approved_reviews.html', context)

@login_required(login_url='/')
def UNAPPROVEDREVIEWS(request):    
    approved_rev = Review.objects.filter( Q(status='Unapproved'))
    paginator = Paginator(approved_rev, 10)  # Show 10 enquiries per page

    page_number = request.GET.get('page')
    try:
        approved_rev = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        approved_rev = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        approved_rev = paginator.page(paginator.num_pages)

    context = {
        'approved_rev': approved_rev,
    }
    return render(request, 'admin/unapproved_reviews.html', context)

@login_required(login_url='/')
def VIEW_REVIEWS(request,id):    
    view_rev = Review.objects.filter(id=id)
      
    context = {
         'view_rev':view_rev,
         
    }
    return render(request,'admin/view-review-details.html',context)

def UPDATE_REVIEW_STATUS(request):
    rev_id = request.POST.get('rev_id')
    status_text = request.POST.get('status')

    try:
        rev_update = Review.objects.get(id=rev_id)
        rev_update.status = status_text
        rev_update.save()

        messages.success(request, "Status updated successfully")
    except Review.DoesNotExist:
        messages.error(request, "Review not found")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('all-reviews')

@login_required(login_url='/')
def DELETE_REVIEWS(request,id):
    del_rev = Review.objects.get(id=id)
    del_rev.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    return redirect('all-reviews')
