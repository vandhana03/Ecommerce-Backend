import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render
import jwt

# from my_project.my_project.settings import SECRET_KEY
from django.conf import settings
SECRET_KEY=settings.SECRET_KEY

from .models import Users,Product
from .serializers import RegisterSerializer, ProductSerializer
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .passwords import check_password, hash_password
from django.forms.models import model_to_dict



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
class RegisterView(View):
    def post(self,req):
        data={
            "username":req.POST.get('username'),
            "password":req.POST.get('password'),
            "email":req.POST.get('email'),
            "role":req.POST.get('role'),
            "address":req.POST.get('address')
        }
        # data['password'] = hash_password(data['password'])
        serializer=RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                "status":True,
                "message":"User registered succesffully",
                "data":serializer.data
            },status=201)
        else:
            print(serializer.errors)
        return JsonResponse(serializer.errors,status=400)
    
@method_decorator(csrf_exempt,name='dispatch')

class LoginView(View):
    def post(self,req):
        username=req.POST.get('username')
        password=req.POST.get('password')

        if not username or not password:
            return JsonResponse({"error":"Missing Credentials"},status=400)
        try:
            user=Users.objects.get(username=username)
        except Users.DoesNotExist:
            return JsonResponse({"error":"user not found"},status=404)
        if not check_password(password,user.password):
            return JsonResponse({"error":"invalid password"},status=401)
        
        payload={
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        }
        token=jwt.encode(payload,SECRET_KEY,algorithm="HS256")

        return JsonResponse({
            "message":"Login successful🎉",
            "token":token,
            "user":{
                "username":user.username,
                "email":user.email,
                "role":user.role
            }
        },status=200)
        


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