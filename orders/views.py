from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem
from cart.models import Cart
from users.models import Users

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
        print("ERROR",e)
        return None
    
@method_decorator(csrf_exempt,name='dispatch')
class CheckoutView(View):
    def post(self,req):
        user=get_user_from_token(req)
        if not user:
            return JsonResponse({"error":"Unauthorized"},status=401)
        cart_items=Cart.objects.filter(user=user)
        if not cart_items.exists():
            return JsonResponse({
                "error":"cart is empty"},
                status=400
                )
        total=0
        #calculate total
        for item in cart_items:
            total += item.product.price * item.quantity
        order=Order.objects.create(
            user=user,
            total_price=total
        )
    #create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        #clear cart
        cart_items.delete()

        return JsonResponse({
            "message":"order placed successfully",
            "order_id":order.id,
            "total":float(total)
        })
@method_decorator(csrf_exempt,name='dispatch')

class OrderListView(View):
    def get(self,req):
        user=get_user_from_token(req)
        if not user:
            return JsonResponse({"error":"unauthorized"},status=401)
        orders=Order.objects.filter(user=user)
        data=[]
        for order in orders:
            items=[]

            for item in order.items.all():
                items.append({
                    "product":item.product.name,
                    "quantity":item.quantity,
                    "price":float(item.price)
                })
            data.append({
                "order_id":order.id,
                "total":float(order.total_price),
                "status":order.status,
                "items":items
                })
        return JsonResponse(data,safe=False)
@method_decorator(csrf_exempt,name='dispatch')     
class UpdateOrderStatusView(View):

    def put(self, request, order_id):

        user = get_user_from_token(request)

        if not user or user.role != 'ADMIN':
            return JsonResponse({"error": "Unauthorized"}, status=401)

        try:
            order = Order.objects.get(id=order_id)

        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)

        import json
        body = json.loads(request.body)

        status_value = body.get('status')

        order.status = status_value
        order.save()

        return JsonResponse({
            "message": "Order status updated"
        })