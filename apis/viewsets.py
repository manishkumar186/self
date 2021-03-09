from rest_framework.response import Response
from rest_framework.decorators import api_view
from apis import serializers
from myapp.models import Contact,add_product

@api_view(["GET","POST","PUT","DELETE",])
def contact_api(request):
    if request.method == "GET":
        if "name" in request.GET:
            id = request.GET.get("name")
            detail = Contact.objects.filter(first_name__contains=id)
        else:
            detail = Contact.objects.all()
        
        obj = serializers.ContactSerializer(detail,many=True)

        dt={
            "message":"{} record found".format(len(obj.data)),
            "data":obj.data,
            
        }
        return Response(dt)
    elif request.method == "POST":
        all_data = request.data
        res = serializers.ContactSerializer(data=all_data)

        if res.is_valid():
            res.post()
            return Response(data={"message":"Thanks for your feedback","data":all_data})
        else:
            return Response(res.errors)

    elif request.method == "PUT":
        all_data = request.data
        res = serializers.ContactSerializer(data=all_data)
        if res.is_valid():
            try:
                con_obj = Contact.objects.get(id=all_data.get("id"))
                con_obj.first_name = all_data.get("first_name")
                con_obj.last_name = all_data.get("last_name")
                con_obj.email_address = all_data.get("email_address")
                con_obj.contact_number = all_data.get("contact_number")
                con_obj.description = all_data.get("description")
                con_obj.save()
                return Response({"message":"Data Updated Successfully"})
            except:
                return Response({"status":"ID Does not exists","message":"Data not update"})
        else:
            return Response(res.error)
    
    elif request.method == "DELETE":
        try:
            id = request.data.get("id")
            Contact.objects.get(id=id).delete()
            return Response({"status":"success","message":"Data deleted successfully"})
        except:
            return Response({"status":"Id does not exits","message":"Data not deleted"})

@api_view(["GET",])
def add_product_api(request):
    if request.method == "GET":
        qryset = add_product.objects.all().order_by("-id")
        all_data = serializers.add_productSerializer(qryset,many=True)
        return Response(all_data.data)