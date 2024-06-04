from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import status as rest_status
from wisata_app.models import (
    User, StatusModel, KategoriProvinsi, KategoriObjekWisata, ObjekWisata, Operasional)
from webservice.serializers import (
    RegisterSerializer, LoginSerializer, KategoriProvinsiSerializer, KategoriObjekWisataSerializer, ObjekWisataSerializer, OperasionalSerializer
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .paginators import CustomPagination
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class LoginView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'status' : 200,
            'message' : 'Selamat anda berhasil masuk...',
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'is_active' : user.is_active,
                'is_admin' : user.is_admin,
            }
        })

class LogoutAPIView(APIView):
    def get(self, request):
        django_logout(request)
        return Response({"detail": "Logout Successful"}, status=status.HTTP_200_OK)
    
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Selamat anda berhasil register...',
                'data' : serializer.data,
            }
            return Response(response_data, status = status.HTTP_201_CREATED)
        return Response({
            'status' : status.HTTP_400_BAD_REQUEST,
            'data' : serializer.errors
        }, status = status.HTTP_400_BAD_REQUEST)
    
    
class KategoriProvinsiListApiView(APIView):

    def get(self, request, *args, **kwargs):
        kategori_provinsi = KategoriProvinsi.objects.all()
        serializer = KategoriProvinsiSerializer(kategori_provinsi, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'provinsi' : request.data.get('provinsi'),
        }
        serializer = KategoriProvinsiSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'massage' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class KategoriObjekWisataListApiView(APIView):

    def get(self, request, *args, **kwargs):
        kategori_objek_wisata = KategoriObjekWisata.objects.all()
        serializer = KategoriObjekWisataSerializer(kategori_objek_wisata, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'kategori' : request.data.get('kategori'),
            'deskripsi' : request.data.get('deskripsi'),
        }
        serializer = KategoriObjekWisataSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'massage' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
class ObjekWisataListApiView(APIView):
    authentication_class = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        objek_wisata = ObjekWisata.objects.select_related('status').\
            filter(status = StatusModel.objects.first())
        serializer = ObjekWisataSerializer(objek_wisata, many=True, )
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Seluruh data berhasil dibaca...',
            'user': str(request.user),
            'auth': str(request.auth),
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'nama': request.data.get('nama'),
            'alamat': request.data.get('alamat'),
            'keterangan': request.data.get('keterangan'),
            'rating': request.data.get('rating'),
            'ulasan': request.data.get('ulasan'),
            'foto': request.data.get('foto'),
            'link_gmaps': request.data.get('link_gmaps'),
            'kategori_provinsi': request.data.get('kategori_provinsi'),
            'kategori_objek_wisata': request.data.get('kategori_objek_wisata'),
        }
        serializer = ObjekWisataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Data created successfully...',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ObjekWisataApiView(APIView):
    def get_object(self, id):
        try:
            return ObjekWisata.objects.get(id = id)
        except ObjekWisata.DoesNotExist:
            return None
    
    def get(self, request, id, *args, **kwargs):
        objek_wisata_instance = self.get_object(id)
        if not objek_wisata_instance:
            return Response(
                {
                    'status' : status.HTTP_404_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status= status.HTTP_400_BAD_REQUEST
            )
        serializer = ObjekWisataSerializer(objek_wisata_instance)
        response = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message' : 'Data retrieve successfully...',
            'data' :serializer.data
        }
        return Response(response, status= status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        objek_wisata_instance = self.get_object(id)
        if not objek_wisata_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )

        data = {
            'nama' : request.data.get('nama'),
            'alamat' : request.data.get('alamat'),
            'keterangan' : request.data.get('keterangan'),
            'rating' : request.data.get('rating'),
            'ulasan' : request.data.get('ulasan'),
            'foto' : request.data.get('foto'),
            'link_gmaps' : request.data.get('link_gmaps'),
            'kategori_provinsi' : request.data.get('kategori_provinsi'),
            'kategori_objek_wisata' : request.data.get('kategori_objek_wisata'),
            'status' : request.data.get('status')
        }
        serializer = ObjekWisataSerializer(instance = objek_wisata_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data updated successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        objek_wisata_instance = self.get_object(id)
        if not objek_wisata_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )

        objek_wisata_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully...'
        }
        return Response(response, status = status.HTTP_200_OK)

class OperasionalApiView(APIView):
    def get_object(self, id):
        try:
            return Operasional.objects.get(id=id)
        except Operasional.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            operasional_instance = self.get_object(id)
            if not operasional_instance:
                return Response(
                    {
                        'status': rest_status.HTTP_404_NOT_FOUND,
                        'message': 'Data not found...',
                    }, status=rest_status.HTTP_404_NOT_FOUND
                )
            serializer = OperasionalSerializer(operasional_instance)
            return Response(serializer.data, status=rest_status.HTTP_200_OK)
        
        operasional = Operasional.objects.all()
        serializer = OperasionalSerializer(operasional, many=True)
        return Response(serializer.data, status=rest_status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'objek_wisata': request.data.get('objek_wisata'),
            'hari_operasional': request.data.get('hari_operasional'),
            'jam_buka': request.data.get('jam_buka'),
            'jam_tutup': request.data.get('jam_tutup'),
            'tarif': request.data.get('tarif'),
            'status': StatusModel.objects.first().pk
        }
        serializer = OperasionalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': rest_status.HTTP_201_CREATED,
                'message': 'Data created successfully...',
                'data': serializer.data
            }
            return Response(response, status=rest_status.HTTP_201_CREATED)

        return Response(serializer.errors, status=rest_status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        operasional_instance = self.get_object(id)
        if not operasional_instance:
            return Response(
                {
                    'status': rest_status.HTTP_400_BAD_REQUEST,
                    'message': 'Data not exists...',
                    'data': {}
                }, status=rest_status.HTTP_400_BAD_REQUEST
            )

        data = {
            'objek_wisata': request.data.get('objek_wisata'),
            'hari_operasional': request.data.get('hari_operasional'),
            'jam_buka': request.data.get('jam_buka'),
            'jam_tutup': request.data.get('jam_tutup'),
            'tarif': request.data.get('tarif'),
            'status': StatusModel.objects.first().pk 
        }
        serializer = OperasionalSerializer(instance=operasional_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': rest_status.HTTP_200_OK,
                'message': 'Data updated successfully...',
                'data': serializer.data
            }
            return Response(response, status=rest_status.HTTP_200_OK)

        return Response(serializer.errors, status=rest_status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        operasional_instance = self.get_object(id)
        if not operasional_instance:
            return Response(
                {
                    'status': rest_status.HTTP_400_BAD_REQUEST,
                    'message': 'Data does not exist...',
                    'data': {}
                }, status=rest_status.HTTP_400_BAD_REQUEST
            )

        operasional_instance.delete()
        response = {
            'status': rest_status.HTTP_200_OK,
            'message': 'Data deleted successfully...'
        }
        return Response(response, status=rest_status.HTTP_200_OK)


class ObjekWisataFilter(generics.ListAPIView):
    queryset = ObjekWisata.objects.all()
    serializer_class = ObjekWisataSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['kategori_provinsi__provinsi', 'kategori_objek_wisata__kategori', ]
    ordering_fields = ['nama']


