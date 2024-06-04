import sys
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

def compress_image(image, filename):
    curr_datetime = datetime.now().strftime('%y%m%d %H%M%S')
    im = Image.open(image)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'jpeg', quality = 50, optimize = True)
    im.seek(0)
    new_image = InMemoryUploadedFile(im_io,'ImageField', '%' + '-' + str(curr_datetime) + '.jpg', 'image/jpeg', sys.getsizeof(im_io), None)

class User(AbstractUser):
    is_admin = models.BooleanField(default= False)

    def is_pengguna(self):
        return not self.is_admin
    
    def __str__(self):
        return str(self.username)


class StatusModel(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
        )
    name = models.CharField(max_length = 50, unique = True)
    description = models.TextField(blank = True, null = True)
    status = models.CharField(max_length= 15, choices= status_choices, default ='Aktif')
    
    def __str__(self):
        return str(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name= 'user_profile', on_delete= models.PROTECT)
    foto = models.ImageField(default= None, upload_to = 'profile_images/', blank= True, null= True)
    status = models.ForeignKey(StatusModel, related_name='status_profil', default=StatusModel.objects.first().pk, on_delete= models.PROTECT)
    user_create = models.ForeignKey(User, related_name='user_create_profile', blank=True, null=True, on_delete= models.SET_NULL)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def save(self, force_insert= True, force_update= True, using= None , update_fields= None , *args, **kwargs):
        if self.id:
            try :
                this = Profile.objects.get(id =self.id)
                if this.foto != self.foto:
                    var_foto = self.foto
                    self.foto = compress_image(var_foto, 'profile')
                    this.foto.delete()
        
            except: pass
            super(Profile, self).save(*args, **kwargs)
        
        else :
            if self.foto :
                var_foto = self.foto
                self.foto = compress_image (var_foto, 'profile')
            super(Profile, self).save(*args, **kwargs)

class KategoriProvinsi(models.Model):
    provinsi = models.CharField(max_length = 50)
    status = models.ForeignKey(StatusModel, related_name= 'status_provinsi', default=StatusModel.objects.first().pk,on_delete= models.PROTECT)

    def __str__(self):
        return self.provinsi
    
class KategoriObjekWisata(models.Model):
    kategori = models.CharField(max_length = 50)
    deskripsi = models.TextField(blank = True, null = True)
    status = models.ForeignKey(StatusModel, related_name= 'status_kategori', default=StatusModel.objects.first().pk,on_delete= models.PROTECT)

    def __str__(self):
        return self.kategori
    

class ObjekWisata(models.Model):
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)
    keterangan = models.TextField(blank = True, null = True)
    rating = models.CharField(max_length=50, choices=RATING_CHOICES)
    ulasan = models.TextField(blank = True, null = True)
    foto = models.ImageField(default= None, upload_to='wisata/images', null=True, blank=True)
    link_gmaps = models.URLField(max_length=200, null=True, blank=True)
    kategori_provinsi = models.ForeignKey(KategoriProvinsi, related_name='provinsi_wisata', blank= True, null= True, on_delete=models.CASCADE)
    kategori_objek_wisata = models.ForeignKey(KategoriObjekWisata, related_name='kategori_wisata', blank= True, null= True, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusModel, related_name= 'status_objek_wisata', default=StatusModel.objects.first().pk,on_delete= models.PROTECT)
    # operasional = models.ForeignKey(Operasional, related_name='operasional_wisata',blank= True, null= True, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.nama 
    
    def save(self, force_insert= True, force_update= True, using= None , update_fields= None , *args, **kwargs):
        if self.id:
            try :
                this = ObjekWisata.objects.get(id =self.id)
                if this.foto != self.foto:
                    var_foto = self.foto
                    self.foto = compress_image(var_foto, 'wisata')
                    this.foto.delete()
        
            except: pass
            super(ObjekWisata, self).save(*args, **kwargs)
        
        else :
            if self.foto :
                var_foto = self.foto
                self.foto = compress_image (var_foto, 'wisata')
            super(ObjekWisata, self).save(*args, **kwargs)
        
class Operasional(models.Model):
    HARI_CHOICES = (
        ('senin-kamis', 'Senin-Kamis'),
        ('senin-jumat', 'Senin-Jumat'),
        ('senin-sabtu', 'Senin-Sabtu'),
        ('senin-minggu', 'Senin-Minggu'),
        ('selasa-kamis', 'Selasa-Kamis'),
        ('selasa-jumat', 'Selasa-Jumat'),
        ('jumat-minggu', 'Jumat-Minggu'),
        ('sabtu-minggu', 'Sabtu-Minggu'),
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),  
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),
    )

    objek_wisata = models.ForeignKey(ObjekWisata, related_name='operasional', blank= True, null= True, on_delete=models.CASCADE)
    hari_operasional = models.CharField(max_length=50, choices=HARI_CHOICES)
    jam_buka = models.TimeField()
    jam_tutup = models.TimeField()
    tarif = models.TextField(blank = True, null = True)
    status = models.ForeignKey(StatusModel, related_name= 'status_operasional', default=StatusModel.objects.first().pk,
                               on_delete= models.PROTECT)
    
    def __str__(self):
        return f"{self.objek_wisata} - {self.hari_operasional}"
    
        


