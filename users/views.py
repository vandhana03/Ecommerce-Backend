import datetime

from django.http import JsonResponse
from django.shortcuts import render
import jwt

# from my_project.my_project.settings import SECRET_KEY
from django.conf import settings
SECRET_KEY=settings.SECRET_KEY

from .models import Users
from .serializers import RegisterSerializer, LoginSerializer
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .passwords import check_password, hash_password


# Create your views here.
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
        


       
        
