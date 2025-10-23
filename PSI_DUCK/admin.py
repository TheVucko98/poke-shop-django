from django.contrib import admin
from .models import *
# Register your models here.
# Autori: Nikola Milosavljevic 0355/2021
#         Aleksandar Vuckovic  0733/2022
admin.site.register(RegistrovanKorisnik)
admin.site.register(Karta)
admin.site.register(InformacijePorudzbine)
admin.site.register(Korpa)
admin.site.register(ListaZelja)