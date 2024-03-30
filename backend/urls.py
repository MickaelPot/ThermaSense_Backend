from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('get/temperature/',views.getTemperature),
    path('admin/', admin.site.urls),
    path('add/user/', views.addUser),
    #path('get/user/', views.getUser),
    path('authorize/user/', views.authorizeUser),
    path('delete/user/', views.deleteUser),
    path('update/user/', views.updateUser),
    path('test/backend/', views.testBackEnd),
    path('token/decrypt/', views.decryptToken),
]
