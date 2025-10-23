import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
# Create your models here.
# Autori: Nikola Milosavljevic 0355/2021
#         Vuk Davidovic        0705/2018

class RegistrovanKorisnik(AbstractUser):
    """
        All registered users
        :model: RegistrovanKorisnik
    """
    slika = models.ImageField(upload_to='imgs/', null=True, verbose_name='Profile picture')

    class Meta:
        db_table = 'RegistrovanKorisnik'

class Karta(models.Model):
    """
            Stores the information about karta
            :model: Karta
        """
    naziv = models.CharField(max_length=20)
    cena = models.FloatField(validators=[MinValueValidator(0)]) #ovo osigurava da ne moze da se unese negativna cena
    opis = models.CharField(max_length=255) #blank=True znaci da je neobavezno polje, cisto radi probe
    brPrimeraka = models.IntegerField(validators=[MinValueValidator(0)],default=1)
    brLajkova = models.IntegerField(validators=[MinValueValidator(0)],default=0)
    brDislajkova = models.IntegerField(validators=[MinValueValidator(0)],default=0)
    slika = models.ImageField(upload_to="imgs/", null=True, verbose_name='Pokemon picture')
    popust = models.IntegerField(validators=[MinValueValidator(0)],default=0)

    """
        Returns the price with the discount
    """
    def cena_sa_popustom(self):
        return self.cena * (1 - self.popust /100)
    class Meta:
        db_table = 'Karta'


class IstorijaKupovine(models.Model):
    """
                Stores the information purchase history
                :model: IstorijaKupovine
            """
    korisnik = models.ForeignKey(RegistrovanKorisnik, on_delete=models.CASCADE)
    karta = models.ForeignKey(Karta, on_delete=models.CASCADE)
    kolicina = models.IntegerField(default=0)
    datum = models.DateField(default=timezone.now)
    vreme = models.TimeField(default=timezone.now)

    class Meta:
        db_table = 'IstorijaKupovine'

class InformacijePorudzbine(models.Model):
    """
                Stores the information about purchase information
                :model: InformacijePorudzbine
            """
    datum = models.DateField(default=timezone.now)
    vreme = models.TimeField(default=timezone.now)
    #varijacija:
    #datum = models.DateTimeField(default=datetime.datetime.now());
    ime = models.CharField(max_length=20)
    prezime = models.CharField(max_length=20)
    adresa = models.CharField(max_length=100)
    grad = models.CharField(max_length=20)
    drzava = models.CharField(max_length=20)
    korisnik = models.ForeignKey(RegistrovanKorisnik, on_delete=models.CASCADE)
    class Meta:
        db_table = 'InformacijePorudzbine'

class Korpa(models.Model):
    """
                Stores the information about the cart
                :model: Korpa
            """
    porudzbina = models.ForeignKey(InformacijePorudzbine, on_delete=models.CASCADE)
    karta = models.ForeignKey(Karta, on_delete=models.CASCADE)
    brojArtikala = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    class Meta:
        unique_together = ('porudzbina', 'karta')
        db_table = 'Korpa'

class ListaZelja(models.Model):
    """
                Stores the information about the wishlist
                :model: ListaZelja
            """
    karta = models.ForeignKey(Karta, on_delete=models.CASCADE)
    korisnik = models.ForeignKey(RegistrovanKorisnik, on_delete=models.CASCADE)
    class Meta:
        # za definisanje toga da na zajednickom nivou moraju da budu unique
        unique_together = ('karta', 'korisnik')
        db_table = 'ListaZelja'

class jeOcenio(models.Model):
    """
                Stores information about the user rating the card
                Related to :model: registrovanKorisnik and :model: karta
                :model: jeOcenio
            """
    MOGUCE_OCENE = [
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
    ]

    karta = models.ForeignKey(Karta, on_delete=models.CASCADE)
    korisnik = models.ForeignKey(RegistrovanKorisnik, on_delete=models.CASCADE)
    ocena = models.IntegerField(choices=MOGUCE_OCENE, default=0)
    class Meta:
        unique_together = ('karta', 'korisnik')
        db_table = 'jeOcenio'