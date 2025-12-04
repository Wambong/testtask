from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Item, ItemImage,  CustomerOrder, CustomerOrderItem, Category, Tag

# Inline model to show ItemImage under Item

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    list_filter = ('parent',)
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1  # Number of empty forms to show

# Custom admin for Item
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    inlines = [ItemImageInline]

# Custom admin for Order

class CustomerOrderItemInline(admin.TabularInline):
    model = CustomerOrderItem
    readonly_fields = ('item', 'quantity', 'item_price', 'total')
    extra = 0

    def total(self, obj):
        return obj.total()


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'name', 'email', 'phone', 'created_at', 'total_price')
    readonly_fields = ('order_number', 'created_at', 'total_price')
    inlines = [CustomerOrderItemInline]
    search_fields = ('order_number', 'name', 'email', 'phone')
    list_filter = ('created_at',)


@admin.register(CustomerOrderItem)
class CustomerOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'item_price', 'total')
    readonly_fields = ('total',)

    def total(self, obj):
        return obj.total()
# Register models
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage)


admin.site.register(Category, CategoryAdmin)

