from .models import Cart, Category

def cart_item_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart = Cart.objects.filter(session_id=session_id).first()

        if cart:
            count = sum(item.quantity for item in cart.items.all())
    except Exception:
        count = 0  # Safe fallback

    return {'cart_item_count': count}

def categories_processor(request):
    return {
        'nav_categories': Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    }
