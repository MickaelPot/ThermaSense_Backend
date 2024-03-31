from datetime import date, datetime, timedelta
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import time


from .serializers import UserSerializer
from .serializers import ReleveSerializer
from .model_releve import Releve
from django.db.models import Q
from .model_user import User
from django.contrib.auth.hashers import make_password, check_password

from .controler_lora import demandeTemperature

from .pompe_evenement import Evenement
from .pompe_evenement import FunctionEvent
import asyncio
from.pompe_evenement import start_function_event_loop

#Pompe à evenements
event_queue = asyncio.Queue()
#start_function_event_loop(event_queue)

#@api_view(['GET'])
def testBackEnd(request):
    return JsonResponse({"message": "Le back end est fonctionnel"},safe=False)

@csrf_exempt
def getTemperature(request):
    if request.method=='GET':
        iot = demandeTemperature()
        if type(iot) == str:
            iot=iot.split('\x00')[0]
        else:
            iot= str(iot)
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


def recuperationPeriodiqueTemperature():
    tm = datetime.now()
    iot = demandeTemperature()
    if type(iot) == str:
        iot=iot.split('\x00')[0]
        temperature = int(iot)
    else:
        temperature = iot
    rel= dict()
    rel["date"]= tm
    rel["temperature"]= temperature
    print("passe dans le cron")

    releve_serializer=ReleveSerializer(data=rel)
    if releve_serializer.is_valid():
        releve_serializer.save()
        return JsonResponse({"message": "success"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)

@csrf_exempt
def handle_event(request):
    event_name = request.POST.get('evenement')
    param = request.POST.get('param')
    function_event = FunctionEvent(event_name, param)
    asyncio.run_coroutine_threadsafe(event_queue.put(function_event), asyncio.get_event_loop())
    return JsonResponse({'status': 'success'})

async def event_loop_startup():
    await start_function_event_loop(event_queue)


@api_view(['GET'])
def getTemperatureByDay(request):
    today = date.today()
    results = Releve.objects.filter(date__contains=today)
    
    tab_results= []

    for resultat in results:
        resultat.date=resultat.date.hour
        tab_results.append(resultat)

    tab_classement = []
    accumulateur = 0
    taille = len(tab_results)
    
    dictionnaire = dict()
    dictionnaire["heure"] = tab_results[0].date
    dictionnaire["cumul"] = 0

    for i in range(taille):
        if tab_results[i].date == dictionnaire["heure"]:
            dictionnaire["cumul"] = dictionnaire["cumul"]+tab_results[i].temperature
            accumulateur=accumulateur+1
        else:
            dictionnaire["cumul"] = round(dictionnaire["cumul"] / accumulateur)
            tab_classement.append(dictionnaire)
            dictionnaire = dict()
            dictionnaire["heure"] = tab_results[i].date
            dictionnaire["cumul"] = tab_results[i].temperature
            accumulateur=1
    dictionnaire["cumul"] = round(dictionnaire["cumul"] / accumulateur)
    tab_classement.append(dictionnaire)

    return JsonResponse({'reponse': tab_classement})

@api_view(['GET'])
def getTemperatureByWeek(request):
    today = datetime.now()
    five_days = today - timedelta(days=5)
    print(five_days)
    tuples_entre_dates = Releve.objects.filter(
        Q(date__gte=five_days) & Q(date__lte=today)
    )

    tab_results= []

    for resultat in tuples_entre_dates:
        resultat.date=str(resultat.date.day) + " "+str(resultat.date.month)
        tab_results.append(resultat)

    tab_classement = []
    accumulateur = 0
    taille = len(tab_results)
    
    dictionnaire = dict()
    dictionnaire["jour"] = tab_results[0].date
    dictionnaire["cumul"] = 0

    for i in range(taille):
        if tab_results[i].date == dictionnaire["jour"]:
            dictionnaire["cumul"] = dictionnaire["cumul"]+tab_results[i].temperature
            accumulateur=accumulateur+1
        else:
            dictionnaire["cumul"] = round(dictionnaire["cumul"] / accumulateur)
            tab_classement.append(dictionnaire)
            dictionnaire = dict()
            dictionnaire["jour"] = tab_results[i].date
            dictionnaire["cumul"] = tab_results[i].temperature
            accumulateur=1
    dictionnaire["cumul"] = round(dictionnaire["cumul"] / accumulateur)
    tab_classement.append(dictionnaire)

    return JsonResponse({'reponse': tab_classement})