from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=250,blank=True)
    last_name = models.CharField(max_length=250,blank=True)
    email_address = models.EmailField(max_length=200,blank=True)
    contact_number = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name+" "+self.last_name

class Category(models.Model):
    cat_name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="categories/%Y/%m/%d")
    desc = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name

class Register(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pic/%Y/%m/%d",null=True,blank=True)
    contact_number = models.IntegerField()
    gender = models.CharField(max_length=250)
    address = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class add_product(models.Model):
    seller_name = models.ForeignKey(User,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_price = models.FloatField()
    sale_price = models.FloatField()
    product_image = models.ImageField(upload_to="products/%Y/%m/%d")
    details = models.TextField()

    def __str__(self):
        return self.product_name

class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(add_product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250)
    product_id = models.CharField(max_length=250,null=True)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username













