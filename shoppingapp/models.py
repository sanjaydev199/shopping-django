# from django.db import models
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import AbstractUser
# from django.utils import timezone
# from django.core.validators import MaxValueValidator, MinValueValidator


# class CustomUser(AbstractUser):
#     USER ={
#         (1,'admin'),
#         (2,'subadmin'),
        
        
#     }
#     user_type = models.CharField(choices=USER,max_length=50,default=1)

#     profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True)

# class Brand(models.Model):
#     brandname = models.CharField(max_length=250,blank=True)
#     brandlogo = models.ImageField(upload_to='logo/brandlogo', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Category(models.Model):
#     catname = models.CharField(max_length=200)
#     catdes = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.catname

# class Subcategory(models.Model):
#     cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcatname = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.subcatname

# class Products(models.Model):
#     cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
#     productname = models.CharField(max_length=250)
#     brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     productpricebd = models.DecimalField(max_digits=10, decimal_places=2)
#     productprice = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     shippingcharge = models.DecimalField(max_digits=10, decimal_places=2)
#     productavailability = models.CharField(max_length=50)
#     productimage1 = models.ImageField(upload_to='media/product_image1', blank=True)
#     productimage2 = models.ImageField(upload_to='media/product_image2', blank=True)
#     productimage3 = models.ImageField(upload_to='media/product_image3', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class RegUsers(models.Model):
#     admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     mobilenumber = models.CharField(max_length=11, unique=True)    
#     joinigdate_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class Cart(models.Model):
#     reguser = models.ForeignKey(RegUsers, on_delete=models.CASCADE)
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)
    
#     def get_total_price(self):
#         return self.product.productprice * self.quantity + self.product.shippingcharge

# class Wishlist(models.Model):
#     reguser = models.ForeignKey(RegUsers, on_delete=models.CASCADE)
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)


# class Order(models.Model):
#     reguser = models.ForeignKey(RegUsers, on_delete=models.CASCADE)
#     billing_address = models.TextField()
#     shipping_address = models.TextField()
#     transaction_method = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     shipping_charge = models.DecimalField(max_digits=10, decimal_places=2)
#     remark = models.CharField(max_length=250)
#     status = models.CharField(max_length=250)
#     updated_at = models.DateTimeField(auto_now=True)
#     def get_total_item_price(self):
#         return self.quantity * self.price + self.shipping_charge



# class Tracking(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_info',null=True)
#     remark = models.CharField(max_length=250,default=0)
#     status = models.CharField(max_length=250,default=0)    
#     updated_at = models.DateTimeField(auto_now=True)


# class Review(models.Model):
#     prod_id = models.ForeignKey(Products, on_delete=models.CASCADE)
#     review = models.TextField()
#     name = models.CharField(max_length=250)
#     email = models.CharField(max_length=250)
#     status = models.CharField(max_length=250, blank=True)
#     rating = models.IntegerField(default=0)  # New rating field
#     posted_date = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.name} - {self.prod_id} - Rating: {self.rating} - Review: {self.review}"

#     def star_rating(self):
#         """Return a string of stars based on the rating."""
#         return "★" * self.rating + "☆" * (5 - self.rating)  # Full stars for rating, empty stars for remaining
    

from django.db import models
from django.contrib.auth.models import AbstractUser

# ------------------ CUSTOM USER ------------------

class CustomUser(AbstractUser):
    USER = {
        (1, 'admin'),
        (2, 'subadmin'),
    }
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True)


# ------------------ BASIC MODELS ------------------

class Brand(models.Model):
    brandname = models.CharField(max_length=250, blank=True)
    brandlogo = models.ImageField(upload_to='logo/brandlogo', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    catname = models.CharField(max_length=200)
    catdes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.catname


class Subcategory(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcatname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subcatname


class Products(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    productname = models.CharField(max_length=250)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    productpricebd = models.DecimalField(max_digits=10, decimal_places=2)
    productprice = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    shippingcharge = models.DecimalField(max_digits=10, decimal_places=2)
    productavailability = models.CharField(max_length=50)
    productimage1 = models.ImageField(upload_to='media/product_image1', blank=True)
    productimage2 = models.ImageField(upload_to='media/product_image2', blank=True)
    productimage3 = models.ImageField(upload_to='media/product_image3', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ------------------ USER PROFILE ------------------

class RegUsers(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11, unique=True, null=True, blank=True)
    joinigdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ------------------ CART & WISHLIST ------------------

class Cart(models.Model):
    reguser = models.ForeignKey(RegUsers, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.product.productprice * self.quantity + self.product.shippingcharge


class Wishlist(models.Model):
    reguser = models.ForeignKey(RegUsers, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


# ------------------ ORDER ------------------

class Order(models.Model):
    reguser = models.ForeignKey(RegUsers, on_delete=models.CASCADE)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    transaction_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.reguser.admin.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_item_price(self):
        return self.quantity * self.price + self.shipping_charge


# ------------------ TRACKING ------------------

class Tracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_info', null=True)
    remark = models.CharField(max_length=250, default=0)
    status = models.CharField(max_length=250, default=0)
    updated_at = models.DateTimeField(auto_now=True)


# ------------------ REVIEW ------------------

class Review(models.Model):
    prod_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    review = models.TextField()
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    status = models.CharField(max_length=250, blank=True)
    rating = models.IntegerField(default=0)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.prod_id} - Rating: {self.rating}"

    def star_rating(self):
        return "★" * self.rating + "☆" * (5 - self.rating)


# ------------------ SIGNAL (MOST IMPORTANT 🔥) ------------------

""" from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        RegUsers.objects.create(admin=instance) """