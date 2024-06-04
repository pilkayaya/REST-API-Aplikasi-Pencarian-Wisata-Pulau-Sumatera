from django.urls import path, include
from webservice import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    RegisterAPIView, LoginView, LogoutAPIView, KategoriProvinsiListApiView, KategoriObjekWisataListApiView, 
    ObjekWisataListApiView,  OperasionalApiView, ObjekWisataFilter 
) 

app_name = 'webservice'
urlpatterns = [
    path('webservice/kategori_provinsi', views.KategoriProvinsiListApiView.as_view()),
    path('webservice/kategori_objek_wisata', views.KategoriObjekWisataListApiView.as_view()),
    path('webservice/objek_wisata', views.ObjekWisataListApiView.as_view()),
    path('webservice/objek_wisata/<int:id>', views.ObjekWisataApiView.as_view()),
    path('webservice/operasional', views.OperasionalApiView.as_view()), 
    path('webservice/operasional/<int:id>', views.OperasionalApiView.as_view()),
    path('webservice/register', views.RegisterAPIView.as_view()),
    path('webservice/login', views.LoginView.as_view()),
    path('webservice/logout', views.LogoutAPIView.as_view()),
    path('webservice/objek_wisata_filter/', views.ObjekWisataFilter.as_view()),

] 