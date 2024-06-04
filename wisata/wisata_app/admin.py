from django.contrib import admin
from wisata_app.models import User, StatusModel, Profile, KategoriProvinsi, KategoriObjekWisata, Operasional, ObjekWisata

admin.site.register(User)
admin.site.register(StatusModel)
admin.site.register(Profile)
admin.site.register(KategoriProvinsi)
admin.site.register(KategoriObjekWisata)
admin.site.register(Operasional)
admin.site.register(ObjekWisata)