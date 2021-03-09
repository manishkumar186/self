from django.urls import path
from apis import viewsets

urlpatterns=[
    path('contact/',viewsets.contact_api),
    path('add_product/',viewsets.add_product_api),
]