from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'items', views.ItemViewSet)
# router.register(r'orders', views.OrderViewSet)
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    # path('add_item/', views.add_item, name='add_item'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path("item/image/<int:image_id>/delete/", views.delete_item_image, name="delete_item_image"),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('product/<int:item_id>/', views.product_detail, name='product_detail'),

    path('api/', include(router.urls)),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('submit_review/<int:item_id>/', views.submit_review, name='submit_review'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/orders/', views.user_orders, name='user_orders'),
    path('dashboard/order/<int:order_id>/', views.order_detail, name='order_detail'),

    # Admin-only URLs
    path('dashboard/admin/orders/', views.all_orders, name='all_orders'),
    path('dashboard/admin/categories/', views.category_management, name='category_management'),
    path('dashboard/admin/tags/', views.tag_management, name='tag_management'),
    path('dashboard/admin/add-category/', views.add_category, name='add_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('dashboard/admin/add-tag/', views.add_tag, name='add_tag'),
    path('dashboard/admin/add_item/', views.add_item, name='add_item'),
    path('order/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),
    path('search/', views.search_view, name='search'),


]