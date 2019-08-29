from django.urls import path,re_path
from . import views

app_name='akun-api'
urlpatterns = [
    path('register/',views.RegisterUserAPIView.as_view(),name='akun-api'),
    path('list/',views.ListUserAPIView.as_view(),name='list-api')
]