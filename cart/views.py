from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Cart
# from products.models import 
from users.models import Product,Users

import json
import jwt
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

# Create your views here.
def get_user_from_token(req):
    auth_header=req.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        token=auth_header.split(" ")[1]
        payload=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        user=Users.objects.get(username=payload['username'])
        return user
    except Exception as e:
         print("ERROR:", e)
         return None

@method_decorator(csrf_exempt,name='dispatch')
class CartView(View):
    def get(self,req):
        user=get_user_from_token(req)
        if not user:
            return JsonResponse({"error":"Unauthorized"},status=401)
        cart_items=Cart.objects.filter(user=user)
        data=[]
        total=0
        for item in cart_items:
            subtotal=item.quantity * item.product.price
            total += subtotal
            data.append({
                "id":item.id,
                "product":item.product.name,
                "price":float(item.product.price),
                "quantity":item.quantity,
                "subtotal":float(subtotal)
            })
        return JsonResponse({
            "cart":data,
            "total":total
        })
    
    #add to cart
    def post(self,req):
        user=get_user_from_token(req)
        if not user:
            return JsonResponse({"error":"unauthorized"},status=401)
        
        body=json.loads(req.body)

        product_id=body.get('product_id')
        quantity=body.get('quantity',1)

        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error":"product not found"},status=404)
        cart_item,created=Cart.objects.get_or_create(
            user=user,
            product=product
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity =quantity
        cart_item.save()
        return JsonResponse({
            "message":"added to cart"
        })


    def put(self,req):
        user=get_user_from_token(req)
        if not user:
            return JsonResponse({"error":"unauthorized"},status=401)
        
        body=json.loads(req.body)
        cart_id=body.get('cart_id')
        quantity=body.get('quantity')

        try:
            cart_item=Cart.objects.get(id=cart_id,user=user)

            cart_item.quantity=quantity
            cart_item.save()

            return JsonResponse({"message":"updated"})
        except Cart.DoesNotExist:
            return JsonResponse({"error":"cart item not found"},status=404)
        
    #delete
    def delete(self,req):
        user=get_user_from_token(req)

        if not user:
            return JsonResponse({"error":"unauthorized"},status=401)
        
        body=json.loads(req.body)
        cart_id=body.get('cart_id')

        try:
            cart_item=Cart.objects.get(id=cart_id,user=user)
            cart_item.delete()
            return JsonResponse({"message":"removed from cart"})
        except Cart.DoesNotExist:
            return JsonResponse({"error":"not found"},status=404)
        

       
