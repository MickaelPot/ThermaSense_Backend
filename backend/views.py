from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from rest_framework_simplejwt.tokens import RefreshToken
import jwt


from .serializers import UserSerializer
from .model_user import User
from django.contrib.auth.hashers import make_password, check_password

from .controler_lora import demandeTemperature

@api_view(['GET'])
def testBackEnd(request):
    return JsonResponse({"message": "Le back end est fonctionnel"},safe=False)

@csrf_exempt
def getTemperature(request):
    if request.method=='GET':
        iot = demandeTemperature()
        data = {
            'temperature': iot,
        }
        return JsonResponse(data,safe=False)
    
@api_view(['POST'])
def addUser(request):
    data = JSONParser().parse(request)
    boolean_valide= False
    try:
        if "mail" in data:
            user = User.objects.get(mail=data["mail"])
            return JsonResponse({"message": "mail existant"},safe=False)
    except User.DoesNotExist:
        boolean_valide=True
    if boolean_valide:
        if("password" in data):
            data["password"]=make_password(data["password"])
        user_serializer=UserSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({"message": "success"},safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)
    
@api_view(['POST'])
def getUser(request):
    data = JSONParser().parse(request)
    if "mail" in data:
        user=User.objects.filter(mail=data["mail"])
        if len(user)>0:
            user=user[0]
            user_serializer=UserSerializer(user)
            return JsonResponse(user_serializer.data,safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)
    
@api_view(['PUT'])
def updateUser(request):
    data = JSONParser().parse(request)
    if "id" in data:
        try:
            user = User.objects.get(pk=data["id"])
        except User.DoesNotExist:
            return JsonResponse({"message": "unsuccess"})
        if("password" in data):
            data["password"]=make_password(data["password"])
        user_serializer=UserSerializer(user, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({"message": "success"},safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)
    
@api_view(['DELETE'])
def deleteUser(request):
    data = JSONParser().parse(request)
    if "mail" in data:
        user=User.objects.filter(mail=data["mail"])
        if len(user)>0:
            user=user[0]
            user.delete()
            return JsonResponse({"message": "success"},safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)


@api_view(['POST'])
def authorizeUser(request):
    data = JSONParser().parse(request)
    if "mail" in data:
        try:
            user = User.objects.get(mail=data["mail"])
            if("password" in data):
                if check_password(data["password"], user.password):
                    token = RefreshToken.for_user(user)
                    token_strng = str(token)
                    return JsonResponse({"message": "success", "token":token_strng},safe=False)
                return JsonResponse({"message": "mot de passe incorrect"},safe=False)
            return JsonResponse({"message": "mot de passe manquant"},safe=False) 
        except User.DoesNotExist:
            return JsonResponse({"message": "compte inexistant"})
    return JsonResponse({"message": "mail manquant"},safe=False)


#@api_view(['POST'])
#def decryptToken(request):
#    data = JSONParser().parse(request)
#    if "token" in data:
#        print(data)
#        token = jwt.decode(
#            request.headers.get('Authorization'),
#            "django-insecure-t0ih7)(l-xk!oprg=2mv+68#_dzdjr_hov$m6k1y%ni%cf*h7&",
#            algorithms=['HS256'])
#        #print(jwt.decode(data, "django-insecure-t0ih7)(l-xk!oprg=2mv+68#_dzdjr_hov$m6k1y%ni%cf*h7&", algorithms=["HS256"]))
#        return JsonResponse({"message": "success"},safe=False)
#    return JsonResponse({"message": "token manquant"},safe=False)

@api_view(['get'])
def decryptToken(request):
    #token = jwt.decode(
    #        request.headers.get('Authorization'),
    #        "django-insecure-t0ih7)(l-xk!oprg=2mv+68#_dzdjr_hov$m6k1y%ni%cf*h7&",
    #        algorithms=['HS256'])
    print('TEST')
    token = request.headers.get('Authorization')
    print(token)
    b = bytearray()
    b.extend(map(ord, token))
    token_decryt = jwt.decode(
            b,
            "django-insecure-t0ih7)(l-xk!oprg=2mv+68#_dzdjr_hov$m6k1y%ni%cf*h7&",
            algorithms=['HS256'])
    print(token_decryt)


#    if "token" in data:
#        print(data)
#        token = jwt.decode(
#            request.headers.get('Authorization'),
#            "django-insecure-t0ih7)(l-xk!oprg=2mv+68#_dzdjr_hov$m6k1y%ni%cf*h7&",
#            algorithms=['HS256'])
#        #print(jwt.decode(data, "django-insecure-t0ih7)(l-xk!oprg=2mv+68#_dzdjr_hov$m6k1y%ni%cf*h7&", algorithms=["HS256"]))
#        return JsonResponse({"message": "success"},safe=False)
    return JsonResponse({"message": "token manquant"},safe=False)