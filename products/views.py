import json

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.views import View
from django.http import JsonResponse
import jwt
from .models import Users,Product
from .serializers import ProductSerializer
from django.conf import settings
SECRET_KEY=settings.SECRET_KEY

# Create your views here.

def get_logged_in_user(request):

    token = request.headers.get('Authorization')

    if not token:
        return None
    try:
        token = token.split(' ')[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        user = Users.objects.get(
            email=payload['email']
        )

        return user

    except:
        return None


@method_decorator(csrf_exempt,name='dispatch')
class ProductListCreateView(View):
    def get(self,req):
        products=Product.objects.all()
        category=req.GET.get('category')
        search=req.GET.get('search')

        if category:
            products=products.filter(category=category)
        if search:
            products=products.filter(name__icontains=search)
        data = list(products.values())
        return JsonResponse(data, safe=False)
    #add product 
    #admin only
    def post(self, req):
        user = get_logged_in_user(req)

        if not user:
            return JsonResponse({
                "error": "Invalid token"
        }, status=401)

        if user.role != "ADMIN":
            return JsonResponse({
                "error": "Only admins can add products"
            }, status=403)

        try:
            body = json.loads(req.body)

        except:
            return JsonResponse({
                "error": "Invalid JSON"
            }, status=400)

        serializer = ProductSerializer(data=body)

        if serializer.is_valid():

            serializer.save()

            return JsonResponse({
                "message": "Product added successfully",
                "data": serializer.data
            }, status=201)

        return JsonResponse(serializer.errors, status=400)
        
@method_decorator(csrf_exempt,name='dispatch')
class ProductDetailView(View):
    #to get single products details by 
    def get(self,req,product_id):
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({
                "error":"product not found"
            },status=404)
        
        return JsonResponse(model_to_dict(product))
    #update product only admin can do it
    def put(self, req, product_id):
        user = get_logged_in_user(req)
        if not user:
            return JsonResponse({
                "error": "Invalid token"
        }, status=401)

        if user.role != "ADMIN":
            return JsonResponse({
                "error": "Only admin can update products"
        }, status=403)

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return JsonResponse({
                "error": "Product not found"
        }, status=404)

        body = json.loads(req.body)

        serializer = ProductSerializer(
            product,
            data=body,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return JsonResponse({
                "message": "Product updated successfully",
                "data": serializer.data
        })

        return JsonResponse(serializer.errors, status=400)

    def delete(self, req, product_id):
        user = get_logged_in_user(req)
        if not user:
            return JsonResponse({
                "error": "Invalid token"
            }, status=401)

        if user.role != "ADMIN":
            return JsonResponse({
                "error": "Only admin can delete products"
            }, status=403)

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return JsonResponse({
                "error": "Product not found"
        }, status=404)

        product.delete()

        return JsonResponse({
            "message": "Product deleted successfully"
    })