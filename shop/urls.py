from django.urls import path, include
# from . import view
from shop.view import views

# Import from the django auth
from django.contrib.auth import views as auth_views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),

    # We don't need to add the above urls if we add this line
    path('', include('django.contrib.auth.urls')),

    # Url for registering users
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    # Product page urls
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

]
