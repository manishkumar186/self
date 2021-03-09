from myapp.models import Contact,Category,add_product,User
from rest_framework import serializers
from django.shortcuts import get_object_or_404

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Contact
        fields = ["id","first_name","last_name","email_address","contact_number","description"]
    
    def post(self):
        Contact.objects.create(**self.validated_data)
        
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name"]

class add_productSerializer(serializers.ModelSerializer):
    product_category = CategorySerializer()
    seller_name = UserSerializer()
    class Meta:
        model = add_product
        fields = "__all__"