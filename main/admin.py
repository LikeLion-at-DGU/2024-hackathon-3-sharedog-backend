from django.contrib import admin
from .models import Sizetest, Agetest, Weighttest, Vaccinetest, Diseasetest, Totaltest
# Register your models here.
admin.site.register(Sizetest)
admin.site.register(Agetest)
admin.site.register(Weighttest)
admin.site.register(Vaccinetest)
admin.site.register(Diseasetest)
admin.site.register(Totaltest)
