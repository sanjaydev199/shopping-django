
from .models import Cart, Wishlist, Category, Products, Order
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def category_processor(request):
    cat = Category.objects.all()
    return {'cat': cat}
    
def wishlist_and_cart_counts(request):
    wishlist_count = 0
    cart_count = 0

    if request.user.is_authenticated:
        try:
            reguser = request.user.regusers
            wishlist_count = Wishlist.objects.filter(reguser=reguser).count()
            cart_count = Cart.objects.filter(reguser=reguser).count()
        except:
            pass

    return {
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
    }





def new_order(request):
    if request.user.is_authenticated:
        try:
            # Get orders with at least one item having empty/null status
            new_orders = Order.objects.filter(
                Q(items__status__isnull=True) | Q(items__status='')
            ).distinct()  # Ensure distinct order IDs only

            logger.debug(f"Found {new_orders.count()} new orders for user {request.user}")

            return {
                'new_order': new_orders,
            }
        except ObjectDoesNotExist:
            logger.warning(f"No new orders found for user {request.user}")
            return {
                'new_order': [],
            }
    else:
        logger.info("User is not authenticated")
        return {}





    