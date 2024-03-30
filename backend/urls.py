from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views

urlpatterns = [
    path('get/temperature/',views.getTemperature),
    path('admin/', admin.site.urls),
    path('add/user/', views.addUser),
    #path('get/user/', views.getUser),
    path('authorize/user/', views.authorizeUser),
    path('delete/user/', views.deleteUser),
    path('update/user/', views.updateUser),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('test/backend/', views.testBackEnd)
]
