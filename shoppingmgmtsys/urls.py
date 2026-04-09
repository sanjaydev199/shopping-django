"""shoppingmgmtsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views,adminviews,userviews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('base1/', views.BASE1, name='base1'),
    path('Index', views.INDEX, name='index'),
    path('Login', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('ResetPassword', views.reset_password, name='reset_password'),
    path('UserLogout', views.UserLogout, name='userlogout'),
    path('Dashboard', views.DASHBOARD, name='dashboard'),
    path('AdminProfile', views.ADMIN_PROFILE, name='admin_profile'),
    path('AdminProfile/update', views.ADMIN_PROFILE_UPDATE, name='admin_profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),
    path('', views.SHOP, name='shop'),
    path('ViewsProductsDetails/<int:id>/', views.VIEWS_PRODUCTS_DETAILS, name='views_products_details'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='wishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist_view'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
   
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
   
    path('order/<int:order_id>/invoice/', views.generate_invoice, name='generate_invoice'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('search-products/', views.SEARCH_PRODUCTS, name='search_products'),
    path('Aboutus', views.ABOUTUS, name='aboutus'),


    #admin panel
    path('Admin/AddBrand', adminviews.ADD_BRAND, name='add_brand'),
    path('Admin/ManageBrand', adminviews.MANAGE_BRAND, name='manage_brand'),
    path('Admin/DeleteBrand/<str:id>', adminviews.DELETE_BRAND, name='delete_brand'),
    path('Admin/UpdateBrand/<str:id>', adminviews.UPDATE_BRAND, name='update_brand'),
    path('Admin/UpdateBrandDetails', adminviews.UPDATE_BRAND_DETAILS, name='update_brand_details'),
    path('Admin/AddCategory', adminviews.ADD_CATEGORY, name='add_category'),
    path('Admin/ManageCategory', adminviews.MANAGE_CATEGORY, name='manage_category'),
    path('Admin/DeleteCategory/<str:id>', adminviews.DELETE_CATEGORY, name='delete_category'),
    path('UpdateCategory/<str:id>', adminviews.UPDATE_CATEGORY, name='update_category'),
    path('UpdateCategoryDetails', adminviews.UPDATE_CATEGORY_DETAILS, name='update_category_details'),
    path('Admin/AddSubcategory', adminviews.ADD_SUBCATEGORY, name='add_subcategory'),
    path('Admin/ManageSubcategory', adminviews.MANAGE_SUBCATEGORY, name='manage_subcategory'),
    path('Admin/DeleteSubcategory/<str:id>', adminviews.DELETE_SUBCATEGORY, name='delete_subcategory'),
    path('UpdateSubcategory/<str:id>', adminviews.UPDATE_SUBCATEGORY, name='update_subcategory'),
    path('UpdateSubcategoryDetails', adminviews.UPDATE_SUBCATEGORY_DETAILS, name='update_subcategory_details'),
    path('Admin/AddProducts', adminviews.ADD_PRODUCTS, name='add_products'),
    path('Admin/ManageProducts', adminviews.MANAGE_PRODUCTS, name='manage_products'),
    path('Admin/DeleteProducts/<str:id>', adminviews.DELETE_PRODUCTS, name='delete_products'),
   
    path('ViewsProducts/<int:id>/', adminviews.VIEWS_PRODUCTS, name='views_products'),
    path('UpdateProducts', adminviews.UPDATE_PRODUCTS, name='updates_products'),
    path('get_subcat/', adminviews.get_subcat, name='get_subcat'),

    path('Admin/NewOrder', adminviews.NEWORDER, name='new_order'),
    path('Admin/InprocessOrder', adminviews.INPROCESSORDER, name='inprocess_order'),
    path('Admin/DispatchOrder', adminviews.DISPATCHORDER, name='dispatch_order'),
    path('Admin/DeliveredOrder', adminviews.DELIVEREDORDER, name='delivered_order'),
    path('Admin/CancelOrder', adminviews.CANCELEDORDER, name='cancel_order'),
    path('Admin/AllOrder', adminviews.ALLORDER, name='all_order'),
    path('Admin/order/<int:order_id>/', adminviews.view_order_detail, name='view_order_detail'),
    path('Admin/UpdateOrder/<str:id>', adminviews.update_order, name='update_order'),
    path('Admin/SearchOrder', adminviews.Search_Order, name='search_order'),
    path('Admin/OrderReport', adminviews.Between_Date_Order_Report, name='order-report'),
    path('Admin/SaleReport', adminviews.sales_report, name='sales-report'),
    path('Admin/RegisteredUsers', adminviews.Registered_Users, name='registered_users'),
    path('Admin/DeleteRegisteredUsers/<str:id>', adminviews.DELETE_REGUSERS, name='delete_regusers'),
    path('Admin/RegisteredUsersOrders/<str:id>', adminviews.REGUSERS_ORDERS, name='regusers-orders'),
     path('Admin/AllReviews', adminviews.ALLREVIEWS, name='all-reviews'),
     path('Admin/ApprovedReviews', adminviews.APPROVEDREVIEWS, name='approved-reviews'),
     path('Admin/UnapprovedReviews', adminviews.UNAPPROVEDREVIEWS, name='unapproved-reviews'),
     path('Admin/NewReviews', adminviews.NEWREVIEWS, name='new-reviews'),
     path('Admin/DeleteReviews/<str:id>', adminviews.DELETE_REVIEWS, name='delete_reviews'),
     path('Admin/ReviewReviews/<str:id>', adminviews.VIEW_REVIEWS, name='view_reviews'),
     path('UpdateReviewsStatus', adminviews.UPDATE_REVIEW_STATUS, name='update-reviews-status'),
    path('thank_you', views.THANKYOU, name='thank_you'),
    


    #Customer Panel 
    path('Customer/Signup', userviews.SIGNUP, name='signup'),
    path('Customer/Password', userviews.Setting, name='setting'),
    path('Customer/UserProfile', userviews.USER_PROFILE, name='user_profile'),
    path('CustomerProfile/update', userviews.USER_PROFILE_UPDATE, name='user_profile_update'),
   
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)