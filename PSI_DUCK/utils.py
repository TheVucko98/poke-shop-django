from .models import *
from django.db.models import F, FloatField, ExpressionWrapper
# Autori: Aleksandar Vuckovic  0733/2022

#Pomocna f-ja sortira Karte prema kriterijumu
# Ako je po ceni "gleda cena sa popustom"
def vratiSortiraneKartePoParametruIzOpcije(request):
    vrstaSorta = request.GET.get('sort_by', 'nameasc')

    if vrstaSorta == 'nameasc':
        karte = Karta.objects.all().order_by('naziv')
    elif vrstaSorta == 'namedesc':
        karte = Karta.objects.all().order_by('-naziv')
    elif vrstaSorta == 'priceasc':
        karte = Karta.objects.annotate(
            adjusted_price=ExpressionWrapper(
                F('cena') - (F('cena') * F('popust') / 100),
                output_field=FloatField()
            )
        ).order_by('adjusted_price')
    elif vrstaSorta == 'pricedesc':
        karte = Karta.objects.annotate(
            adjusted_price=ExpressionWrapper(
                F('cena') - (F('cena') * F('popust') / 100),
                output_field=FloatField()
            )
        ).order_by('-adjusted_price')
    else:
        karte = Karta.objects.all()

    return karte
