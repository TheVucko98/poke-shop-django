from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# Autori: Nikola Milosavljevic 0355/2021
#         Aleksandar Vuckovic  0733/2022
#         Mihajlo Milojevic    0317/2021



urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls), # To radimo tek kada funkcionalnosti
    path('', include('PSI_DUCK.urls')),
]



# STATIC_URL je da bi uzimali slike i fajlove .js, .css
# MEDIA_URL je za "slike" koje mi dodajemo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
