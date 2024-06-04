from rest_framework import serializers
from wisata_app.models import (
    User, StatusModel, Profile, KategoriProvinsi, KategoriObjekWisata, ObjekWisata, Operasional
)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active and user.is_admin:
                    data['user'] = user
                else:
                    msg = 'Status pengguna tidak aktif...'
                    raise ValidationError({'message': msg})
            else:
                msg = 'Anda tidak memiliki akses masuk...'
                raise ValidationError({'message': msg})
        else:
            msg = 'Anda harus mengisi username dan password...'
            raise ValidationError({'message': msg})
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset = User.objects.all())])
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'is_active', 'is_admin', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password' : 'Password dan Ulang password tidak sama...'
            })
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            is_active = validated_data['is_active'],
            is_admin = validated_data.get('is_admin', False),
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'], 
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class KategoriProvinsiSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name')

    class Meta:
        model = KategoriProvinsi
        fields = ('id', 'provinsi', 'status')
    
class KategoriObjekWisataSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name')

    class Meta:
        model = KategoriObjekWisata
        fields = ('id', 'kategori', 'deskripsi', 'status')

class OperasionalSerializer(serializers.ModelSerializer):
    objek_wisata = serializers.CharField(source='objek_wisata.nama')
    status = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Operasional
        fields = ('id', 'objek_wisata', 'hari_operasional', 'jam_buka', 'jam_tutup', 'tarif', 'status')
        read_only_fields = ('status',)

    def create(self, validated_data):
        status_instance = StatusModel.objects.first() 
        validated_data['status'] = status_instance
        return Operasional.objects.create(**validated_data)
    
class ObjekWisataSerializer(serializers.ModelSerializer):
    # kategori_provinsi = serializers.CharField(source='kategori_provinsi.provinsi')
    # kategori_objek_wisata = serializers.CharField(source='kategori_objek_wisata.kategori')
    status = serializers.CharField(source='status.name', read_only=True)
    operasional = OperasionalSerializer(many=True, read_only=True)

    class Meta:
        model = ObjekWisata
        fields = ('id', 'nama', 'alamat', 'keterangan', 'rating', 'ulasan', 'foto', 'link_gmaps', 'kategori_provinsi', 'kategori_objek_wisata', 'status', 'operasional')
        read_only_fields = ('status',)

    def create(self, validated_data):
        return ObjekWisata.objects.create(**validated_data)

