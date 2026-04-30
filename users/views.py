from django.http import JsonResponse
from django.shortcuts import render
from .models import Users
from .serializers import RegisterSerializer
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
