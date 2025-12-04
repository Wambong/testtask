from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.conf import settings

from django.utils.timezone import now
from django.utils.timezone import localtime
from django.utils.text import slugify
from django.db.models import Avg, Count

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, editable=False)  # not editable
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True,
        help_text="Parent category, leave blank if this is a top-level category."
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_qty = models.PositiveIntegerField(default=0, help_text="Minimum quantity for wholesale discount")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Wholesale discount percentage")
    stock = models.PositiveIntegerField(default=10, help_text="Available stock")
    brand = models.CharField(max_length= 250, blank=True, null=True)
    body = RichTextUploadingField(null=True, blank=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    tags = models.ManyToManyField(Tag, blank=True, related_name='items')

    def __str__(self):
        return f"{self.name} - ${self.price}"

    @property
    def wholesale_price(self):
        """Returns the wholesale price regardless of quantity — useful for displaying"""
        if self.wholesale_qty and self.discount_percentage:
            discount = self.price * self.discount_percentage / 100
            return self.price - discount
        return None
    def averageReview(self):
        reviews = ReviewRating.objects.filter(item=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(item=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="items/extra/")

    def __str__(self):
        return f"Image for {self.item.name}"


class ReviewRating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name='carts'
    )
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart (Session: {self.session_id})"

    @property
    def total_price(self):
        # return sum(item.total_price for item in self.items.all())
        # This will now correctly sum up the total_price from each CartItem
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in cart"
    @property
    def effective_unit_price(self):
        """Returns the unit price after considering wholesale discounts."""
        if self.quantity >= self.item.wholesale_qty and self.item.wholesale_price is not None:
            return self.item.wholesale_price
        return self.item.price
    @property
    def total_price(self):
        # return self.quantity * self.item.price
        """Returns the total price for this cart item, applying wholesale discount if applicable."""
        return self.quantity * self.effective_unit_price


class CustomerOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_number = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            super().save(*args, **kwargs)  # Save first to generate `id` and `created_at`
            local_created = localtime(self.created_at)
            self.order_number = f"ORD-{self.id:05d}-{local_created.strftime('%Y%m%d%H%M%S')}"
            # Update with order number
            CustomerOrder.objects.filter(pk=self.pk).update(order_number=self.order_number)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.name}"

class CustomerOrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # unit price
    is_wholesale = models.BooleanField(default=False)

    def total(self):
        if self.quantity is not None and self.item_price is not None:
            return self.quantity * self.item_price
        return 0

    def __str__(self):
        return f"{self.quantity} x {self.item.name} (Order #{self.order.id})"



