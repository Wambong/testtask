from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from rest_framework import viewsets
# from .serializers import ItemSerializer, OrderSerializer
from django.utils.timezone import now, localtime, make_aware
from datetime import timedelta
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .utils import render_to_pdf
from django.db.models import Sum, Count
from django.shortcuts import render
from django.db.models import Q
User = get_user_model()
from django.db import transaction
from django.db.models import F

from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Item

from django.core.paginator import Paginator

def admin_check(user):
    return user.is_staff



def custom_403(request, exception=None):
    return render(request, '403.html', status=403)

def home(request):
    item_list = Item.objects.all().order_by('id')
    paginator = Paginator(item_list, 16)  # 12 items per page
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    return render(request, 'orders/home.html', {'items': items})


def index(request):
    items = Item.objects.all()
    return render(request, 'orders/index.html', {'items': items})
def product_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item_tags = item.tags.all()
    reviews = ReviewRating.objects.filter(pk=item_id, status=True)
    # Find related items that share any of these tags, excluding the current item
    related_items = Item.objects.filter(tags__in=item_tags).exclude(id=item.id).distinct()[:8]
    context = {
        'reviews': reviews,
        'item': item,
        'related_items': related_items,
    }

    return render(request, 'orders/product-detail.html', context)


# def item_detail(request, item_id):
#     item = get_object_or_404(Item, pk=item_id)
#     item_tags = item.tags.all()
#     reviews = ReviewRating.objects.filter(pk=item_id, status=True)
#     # Find related items that share any of these tags, excluding the current item
#     related_items = Item.objects.filter(tags__in=item_tags).exclude(id=item.id).distinct()[:8]
#     context =  {
#         'reviews': reviews,
#         'item': item,
#         'related_items': related_items,
#     }
#
#     return render(request, 'orders/item_detail.html', context)
def item_detail(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        # Works even when DEBUG = True
        return render(request, '404.html', status=404)

    item_tags = item.tags.all()
    reviews = ReviewRating.objects.filter(pk=item_id, status=True)

    # Find related items that share any of these tags, excluding the current item
    related_items = Item.objects.filter(tags__in=item_tags)\
                                .exclude(id=item.id)\
                                .distinct()[:8]

    context = {
        'reviews': reviews,
        'item': item,
        'related_items': related_items,
    }

    return render(request, 'orders/item_detail.html', context)
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        additional_images = request.FILES.getlist('additional_images')

        if form.is_valid():
            item = form.save()
            for img in additional_images:
                ItemImage.objects.create(item=item, image=img)
            return redirect('add_item')
    else:
        form = ItemForm()
    return render(request, 'dashboard/admin/add_item.html', {'form': form})

@login_required
def add_category(request):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('add_category')  # or use a list view like 'view_all_categories'
    else:
        form = CategoryForm()
    return render(request, 'dashboard/admin/add_category.html', {'form': form})

def edit_item(request, item_id):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        additional_images = request.FILES.getlist('additional_images')

        if form.is_valid():
            item = form.save()  # saves instance

            for img in additional_images:
                ItemImage.objects.create(item=item, image=img)

            messages.success(request, "Item updated successfully.")
            return redirect('home')
        else:
            # 👇 print errors in console AND show them in template
            print("Form errors:", form.errors)
            messages.error(request, f"Fix errors before saving: {form.errors}")
    else:
        form = ItemForm(instance=item)

    return render(request, 'dashboard/admin/edit_item.html', {'form': form, 'item': item})



@login_required
def delete_item_image(request, image_id):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)

    image = get_object_or_404(ItemImage, id=image_id)
    item_id = image.item.id
    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect("edit_item", item_id=item_id)

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id, user=None)
    return cart


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('item').all()
    grand_total = cart.total_price
    return render(request, 'orders/cart.html', {'cart': cart, 'items': items, 'grand_total': grand_total})


def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{item.name} added to cart.")
    return redirect('home')

@require_POST
def update_cart_quantity(request, item_id, action):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).first()

    if not cart:
        return redirect('cart')

    cart_item = cart.items.filter(item_id=item_id).first()
    if not cart_item:
        return redirect('cart')

    if action == 'increment':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrement':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

    return HttpResponseRedirect(reverse('cart'))


@require_POST
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).first()

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    cart_item = cart.items.filter(item_id=item_id).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        messages.warning(request, "Item not found in your cart.")

    return HttpResponseRedirect(reverse('cart'))




def checkout(request):
    # Get cart (by user or session)
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart = Cart.objects.filter(session_id=request.session.session_key).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create CustomerOrder
                order = CustomerOrder.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    country=form.cleaned_data['country'],
                    state=form.cleaned_data['state'],
                    total_price=cart.total_price,
                )

                for cart_item in cart.items.select_related('item').all():
                    item = cart_item.item
                    quantity = cart_item.quantity

                    # Ensure stock is sufficient
                    if item.stock < quantity:
                        messages.error(request, f"Insufficient stock for {item.name}. Only {item.stock} left.")
                        transaction.set_rollback(True)
                        return redirect('cart')

                    # Determine pricing
                    if item.wholesale_qty and quantity >= item.wholesale_qty:
                        item_price = item.wholesale_price
                        is_wholesale = True
                    else:
                        item_price = item.price
                        is_wholesale = False

                    # Create the order item
                    CustomerOrderItem.objects.create(
                        order=order,
                        item=item,
                        quantity=quantity,
                        item_price=item_price,
                        is_wholesale=is_wholesale
                    )

                    # Reduce item stock
                    item.stock = F('stock') - quantity
                    item.save()

                # Delete cart after successful order
                cart.items.all().delete()
                cart.delete()

                messages.success(request, f"Order placed successfully! Your order number is {order.order_number}")
                return redirect('checkout_success')
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

def checkout_success(request):
    return render(request, 'orders/checkout_success.html')

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = category.items.all()
    return render(request, 'orders/category_detail.html', {'category': category, 'items': items})


def submit_review(request, item_id):
    # Get the referring URL or fall back to item detail page
    url = request.META.get('HTTP_REFERER') or reverse('item_detail', args=[item_id])

    # Ensure session exists
    if not request.session.session_key:
        request.session.create()

    if request.method == 'POST':
        try:
            # Try to get existing review
            if request.user.is_authenticated:
                reviews = ReviewRating.objects.get(user=request.user, item__id=item_id)
            else:
                reviews = ReviewRating.objects.get(session_key=request.session.session_key, item__id=item_id)

            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.item_id = item_id
                data.ip = request.META.get('REMOTE_ADDR')

                if request.user.is_authenticated:
                    data.user = request.user
                else:
                    data.session_key = request.session.session_key

                data.save()
                messages.success(request, 'Thank you for your review!')
                return redirect(url)
        except Exception as e:
            messages.error(request, f'Error occurred: {str(e)}')

    # If we get here, something went wrong
    return redirect(url)


@login_required
def dashboard(request):
    context = {}

    if request.user.is_staff:
        from django.utils import timezone
        from datetime import timedelta

        # Basic stats
        total_orders = CustomerOrder.objects.count()
        total_revenue = CustomerOrder.objects.aggregate(
            total=Sum('total_price')
        )['total'] or 0

        # Time-based stats
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)

        recent_orders = CustomerOrder.objects.order_by('-created_at')[:5]
        today_orders = CustomerOrder.objects.filter(
            created_at__date=today
        ).count()
        weekly_revenue = CustomerOrder.objects.filter(
            created_at__date__gte=week_ago
        ).aggregate(
            total=Sum('total_price')
        )['total'] or 0

        context.update({
            'total_orders': total_orders,
            'total_revenue': f"${total_revenue:,.2f}",
            'today_orders': today_orders,
            'weekly_revenue': f"${weekly_revenue:,.2f}",
            'recent_orders': recent_orders,
        })

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def user_orders(request):
    if request.user.is_staff:
        orders = CustomerOrder.objects.all().order_by('-created_at')
    else:
        orders = CustomerOrder.objects.filter(
            user=request.user
        ).order_by('-created_at')
    return render(request, 'dashboard/orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(CustomerOrder, id=order_id)
    else:
        order = get_object_or_404(CustomerOrder, id=order_id, user=request.user)
    return render(request, 'dashboard/order_detail.html', {'order': order})
# Admin views


@login_required
def all_orders(request):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)

    orders = CustomerOrder.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin/all_orders.html', {'orders': orders})

@login_required

def category_management(request):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)

    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'dashboard/admin/categories.html', {'categories': categories})

@login_required

def tag_management(request):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)

    tags = Tag.objects.all()
    return render(request, 'dashboard/admin/tags.html', {'tags': tags})


@login_required

def edit_category(request, pk):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)

    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category_management')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/admin/add_category.html', {"form": form, "title": "Edit Category"})

@login_required
def delete_category(request, pk):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category_management')
    return render(request, 'dashboard/admin/category_confirm_delete.html', {"category": category})
@login_required

def add_tag(request):
    if not admin_check(request.user):
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag added successfully.')
            return redirect('add_tag')  # or use a list view like 'view_all_tags'
    else:
        form = TagForm()
    return render(request, 'dashboard/admin/add_tag.html', {'form': form})





def download_invoice(request, order_id):
    order = get_object_or_404(CustomerOrder, id=order_id)

    # Check permission - only staff or order owner can download invoice
    if not request.user.is_staff and order.email != request.user.email:
        return HttpResponse('Not authorized', status=401)

    pdf = render_to_pdf('dashboard/invoice.html', {
        'order': order,
        'request': request
    })

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Invoice_{order.order_number}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF", status=500)

def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Item.objects.filter(
            Q(name__icontains=query) |
            Q(body__icontains=query) |
            Q(price__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'orders/search_results.html', {
        'query': query,
        'results': results
    })

