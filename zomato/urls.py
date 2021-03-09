"""zomato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('apis.urls')),
    path('',views.home,name="home"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('category',views.navbar,name="navbar"),
    path('login',views.user_login,name="login"),
    path('register',views.register,name="register"),
    path('check_usename',views.check_user,name="check_username"),
    path('verify_email_otp',views.verify_email_otp,name="verify_email_otp"),
    path('cust_dashboard',views.cust_dashboard,name="cust_dashboard"),
    path('logout',views.user_logout,name="logout"),
    path('cust_view',views.cust_view,name="cust_view"),
    path('edit_profile',views.edit_profile,name="edit_profile"),
    path('change_password',views.change_password,name="change_password"),
    path('add_product_view',views.add_product_view,name="add_product_view"),
    path('my_product',views.my_product,name="my_product"),
    path('single_product',views.single_product,name="single_product"),
    path('edit_product',views.edit_product,name="edit_product"),
    path('delete_product',views.delete_product,name="delete_product"),
    path('all_product',views.all_product,name="all_product"),
    path('cart_view',views.cart_view,name="cart_view"),
    path('get_cart_data',views.get_cart_data,name="get_cart"),
    path('change_quantity',views.change_quan,name="change_quan"),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process_payment',views.process_payment,name="process_payment"),
    path('payment_done',views.payment_done,name="payment_done"),
    path('payment_cancelled',views.payment_cancelled,name="payment_cancelled"),
    path('order_history',views.order_history,name="order_history"),
    path('my_customer',views.my_customer,name="my_customer"),
    path('forgot_password',views.forgot_password,name="forgot_password"),
    path('reset_password',views.reset_password,name="reset_password"),
    

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
