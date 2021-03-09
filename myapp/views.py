from django.shortcuts import render,get_object_or_404,reverse
from myapp.models import Contact,Category,Register,add_product,cart,Order
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.core.mail import EmailMessage
from validate_email import validate_email
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
import time


def home(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    data = Category.objects.all().order_by("cat_name")
    context["all_data"]=data   
    return render(request,"home.html",context)

def about(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    return render(request,"about.html",context)

def contact(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    fetch_data = Contact.objects.all().order_by("-id")[:10]
    context["all_data"] = fetch_data
    
    if request.method == "POST":
        f_name = request.POST["fname"]
        l_name = request.POST["lname"]
        email_addr = request.POST["email"]
        phone = request.POST["contact"]
        desc = request.POST["description"]
        
        data = Contact(first_name=f_name,last_name=l_name,email_address=email_addr,contact_number=phone,description=desc)
        data.save()
        context["data"]="Dear Mr/Mis {} {} thanks for feedback...".format(f_name,l_name)
        return render(request,"contact.html",context)
        
    return render(request,"contact.html",context)

def navbar(request):
    context=[]
    data = Category.objects.all()
    context["datas"]=datas
    return render(request,"include/navbar.html",context)


def user_login(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    if request.method == "POST":
        user_name = request.POST["uname"]
        pass_wrd = request.POST["pwd"]

        uname = authenticate(username=user_name,password=pass_wrd)
        if uname:
            login(request,uname)
            if uname.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                return HttpResponseRedirect("/cust_dashboard")
        else:
            context["status"]="Invalid username and password !!!"
            return render(request,"home.html",context)
    return render(request,"login.html",context)

def register(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    if request.method == "POST":
        f_name = request.POST["fname"]
        l_name = request.POST["lname"]
        user_name = request.POST["uname"]
        pass_word = request.POST["password"]
        contact_no = request.POST["contact"]
        email_address = request.POST["email"]
        user_otp = request.POST["otp"]
        gen = request.POST["gender"]
        user_type = request.POST["utype"]
        addr = request.POST["textarea"]
        match_otp = request.POST["motp"]

        if user_otp == match_otp:
            usr = User.objects.create_user(user_name,email_address,pass_word)
            usr.first_name = f_name
            usr.last_name = l_name
            if user_type == "seller":
                usr.is_staff = True
            usr.save()
            data = Register(user=usr,contact_number=contact_no,gender=gen,address=addr)
            data.save()
            context["message"] = "Dear {} {} Signup Successfully".format(f_name,l_name)
            return render(request,"register.html",context)
        elif user_otp != match_otp:
            context["message"] = "Dear {} {} Please Enter Valid otp".format(f_name,l_name)
            return render(request,"register.html",context)
    return render(request,"register.html",context)

def check_user(request):
    if request.method == "GET":
        c_user = request.GET["usern"]
        check = User.objects.filter(username=c_user)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

import random
def verify_email_otp(request):
    if request.method =="GET":
        email_user = request.GET["email"]
        is_valid = validate_email(email_user,verify=True)
        if is_valid !=True:
            return JsonResponse({"status":"invalidEmail","email":email_user})
        else:
            otp = random.randint(1000,9999)
            otps = str(otp)
            try:
                email = EmailMessage("Account verification",otps,to=[email_user])
                email.send()
                return JsonResponse({"status":"sent","rotp":otp,"email":email_user})
            except:
                return JsonResponse({"status":"error"})
            
@login_required    
def cust_dashboard(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic

    return render(request,"cust_dashboard.html",context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def cust_view(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    data = Register.objects.filter(user__id = request.user.id)
    context["all_data"]=data

    check = Register.objects.get(user__id=request.user.id)
    context["register_data"]=check
    return render(request,"cust_view.html",context)

@login_required
def edit_profile(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    check = Register.objects.get(user__id=request.user.id)
    context["register_data"]=check

    user = User.objects.get(id = request.user.id)
    context["user_data"]=user

    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        username = request.POST["uname"]
        gender = request.POST["gender"]
        address = request.POST["textarea"]

        check.contact_number=contact
        check.gender=gender
        check.address=address
        check.save()

        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.username=username
        user.save()
        if "image" in request.FILES:
            pic = request.FILES["image"]
            check.profile_pic=pic
            check.save()
        context["status"]="Update data successfully !!!"
        return render(request,"edit_profile.html",context)
        
    
    return render(request,"edit_profile.html",context)

@login_required
def change_password(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic

    if request.method == "POST":
        current_password = request.POST["cpwd"]
        new_password = request.POST["npwd"]
        check_user_psd = User.objects.get(id=request.user.id)
        un = check_user_psd.username

        check = check_user_psd.check_password(current_password)

        if check == True:
            check_user_psd.set_password(new_password)
            check_user_psd.save()
            context["status"]="password change successfully"
            context["alert"]="text-success"

            user_login = User.objects.get(username=un)
            login(request,user_login)
            return render(request,"change_password.html",context)
        else:
            context["status"]="Please enter valid username"
            context["alert"]="text-danger"
            return render(request,"change_password.html",context)

    return render(request,"change_password.html",context)

@login_required
def add_product_view(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    data = Category.objects.all()
    context["data"]=data

    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic

    if request.method == "POST":
        product_name = request.POST["pname"]
        product_category = request.POST["pcategory"]
        product_price = request.POST["pprice"]
        sale_price = request.POST["sprice"]
        desc = request.POST["desc"]

        if "pimage" in request.FILES:
            product_image = request.FILES["pimage"]

        manish = User.objects.get(username=request.user.username)
        rahul = Category.objects.get(cat_name=product_category)
        

        add_product_data = add_product(seller_name = manish,product_category=rahul,product_name=product_name,product_price=product_price,sale_price=sale_price,details=desc,product_image=product_image)
        add_product_data.save()
        context["status"]="product added successfully"
        return render(request,"add_product.html",context)
    return render(request,"add_product.html",context)

@login_required
def my_product(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic

    obj = add_product.objects.filter(seller_name__id=request.user.id)
    context["obj"]=obj
    return render(request,"my_product.html",context)


def single_product(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    if "pid" in request.GET:
        id = request.GET["pid"]
        obj = add_product.objects.get(id=id)
        context["obj"]=obj

    return render(request,"single_product.html",context)

@login_required
def edit_product(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    cat = Category.objects.all().order_by("cat_name")
    context["cat"]=cat

    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic
    
    objects = request.GET["pid"]
    data = get_object_or_404(add_product,id=objects)
    context["data"]=data

    
    if request.method=="POST":
        product_name = request.POST["pname"]
        product_category = request.POST["pcat"]
        product_price = request.POST["pprice"]
        sale_price = request.POST["sprice"]
        product_desc = request.POST["desc"]

        cats = Category.objects.get(cat_name=product_category)
        
        obj = add_product.objects.get(id=objects)
        obj.product_name=product_name
        obj.product_category=cats
        obj.product_price=product_price
        obj.sale_price=sale_price
        obj.details=product_desc

        if "pimage" in request.FILES:
            product_image = request.FILES["pimage"]
            obj.product_image=product_image
        obj.save()

        context["status"]="update data successfully"
        context["refresh"]=objects
        return render(request,"edit_product.html",context)
        
    return render(request,"edit_product.html",context)

@login_required
def delete_product(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic

    product_id = request.GET["pid"]
    obj = add_product.objects.get(id=product_id)
    context["obj"]=obj
    
    if "action" in request.GET:
        obj.delete()
        context["status"]="{} delete successfully".format(obj.product_name)
        return render(request,"delete_product.html",context)

    return render(request,"delete_product.html",context)

def all_product(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    datas = Category.objects.all()
    context["datas"]=datas

    data = add_product.objects.all()
    context["data"]=data

    if "qry" in request.GET:
        q =request.GET["qry"]
        prd = add_product.objects.filter(Q(product_name__icontains=q)|Q(product_category__cat_name__icontains=q))
        context["data"]=prd

    if "pid" in request.GET:
        pid = request.GET["pid"]
        
        obj = add_product.objects.filter(product_category__id=pid)
        context["data"]=obj
        return render(request,"all_product.html",context)
        
    return render(request,"all_product.html",context)

@login_required
def cart_view(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    items = cart.objects.filter(user__id=request.user.id,status=False)
    context["items"]=items

    if request.user.is_authenticated:
        if request.method=="POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"]

            is_exists = cart.objects.filter(product__id=pid,user__id=request.user.id,status=False)
            if(len(is_exists)>0):
                context["msz"]="item already exits in your card"
                context["cls"]="alert alert-warning"
            else:
                product = get_object_or_404(add_product,id=pid)
                usr = get_object_or_404(User,id=request.user.id)
                c = cart(user=usr,product=product,quantity=qty)
                c.save()
                context["msz"]="{} Added in your cart".format(product.product_name)
                context["cls"]="alert alert-success"
    else:
        context["status"]="Please Login to view your cart"
        
    return render(request,"cart.html",context)

def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id,status=False)
    sale,total,qty=0,0,0
    for i in items:
        sale = sale+(i.product.sale_price)*i.quantity
        total = total+(i.product.product_price)*i.quantity
        qty = qty+i.quantity
    res={
        "total":total,"sale":sale,"qty":qty
    }
    return JsonResponse(res)

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity=qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)
    
    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
def process_payment(request):
    item = cart.objects.filter(user__id=request.user.id,status=False)
    product =""
    amt = 0
    inv = "INV-"
    cart_id = "" 
    product_id = ""
    for i in item:
        product += i.product.product_name+","
        product_id +=str(i.product.id)+","
        amt += (i.product.sale_price)*i.quantity
        inv += str(i.id)
        cart_id += str(i.id)+"," 
        
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': product,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format('127.0.0.1:8000',
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format('127.0.0.1:8000',
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format('127.0.0.1:8000',
                                              reverse('payment_cancelled')),
        
    }
    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr,cart_id=cart_id,product_name=product,product_id=product_id)
    ord.save()
    ord.invoice_id =inv+str(ord.id)
    ord.save()
    request.session["order_id"]=ord.id

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,'process_payment.html', {'form': form})


def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order,id=order_id)
        ord_obj.status=True
        ord_obj.save()

        for i in ord_obj.cart_id.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()

    return render(request,"payment_done.html")

def payment_cancelled(request):
    return render(request,"payment_cancel.html")


@login_required
def order_history(request):
    context={}
    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic

    all_order=[]
    order = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")
    for i in order:
        product = []
        for j in i.product_id.split(",")[:-1]:
            pro = get_object_or_404(add_product,id=j)
            product.append(pro)
        ord={
            "order_id":i.id,
            "product":product,
            "invoice":i.invoice_id,
            "status":i.status,
            "date":i.processed_on,

        }
        all_order.append(ord)
    context["order_history"]=all_order
    return render(request,"order_history.html",context)

@login_required
def my_customer(request):
    context={}
    today_date = date.today()
    curr_time = time.strftime("%H:%M:%S")
    context["date"]=today_date
    context["time"]=curr_time

    pic = Register.objects.get(user__id = request.user.id)
    context["register_data"]=pic

    product = cart.objects.filter(product__seller_name=request.user.id,status=True)
    customer = []
    ids = []
    for i in product:
        us={
            "username":i.user.username,
            "first_name":i.user.first_name,
            "last_name":i.user.last_name,
            "email":i.user.email,

        }
        check = Register.objects.filter(user__id=i.user.id)
        if(len(check)>0):
            prf = get_object_or_404(Register,user__id=i.user.id)
            us["profile_pic"]=prf.profile_pic
            us["contact_number"]=prf.contact_number
            us["join_date"]=prf.added_on
        ids.append(i.user.id)
        count = ids.count(i.user.id)
        if count<2:
            customer.append(us)
    context["customer"]=customer
    return render(request,"my_customer.html",context)

def forgot_password(request):
    context={}
    if request.method == "POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user=get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()
        context["status"]="password change successfully"
    return render(request,"forgot_password.html",context)

import random
def reset_password(request):
    un = request.GET["user"]
    try:     
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "Dear {} \n {} Here one time password (OTP) \nDo not share with other \nThanks for zayka...".format(user.username,otp)
        try:
            email =EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})

