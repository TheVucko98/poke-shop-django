import datetime
import re

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import reverse
from .models import *
import os


def create_user_with_image():
    # Path to the test image in the static directory
    image_path = os.path.join(settings.BASE_DIR, 'PSI_DUCK', 'static', 'img', 'articuno.png')

    # Open the test image and create a SimpleUploadedFile
    with open(image_path, 'rb') as image_file:
        image = SimpleUploadedFile(
            name='articuno.png',
            content=image_file.read(),
            content_type='image/png'
        )
        # Create a user with the uploaded image
        user = RegistrovanKorisnik(username='testuser', slika=image)
        user.set_password('nikola2024')
        user.save()

        # Ensure the 'moderator' group exists, then add the user to the group
        group, created = Group.objects.get_or_create(name='moderator')
        user.groups.add(group)

    return user


def create_karta():
    # Path to the test image in the static directory
    image_path = os.path.join(settings.BASE_DIR, 'PSI_DUCK', 'static', 'img', 'articuno.png')

    # Open the test image and create a SimpleUploadedFile
    with open(image_path, 'rb') as image_file:
        image = SimpleUploadedFile(
            name='articuno.png',
            content=image_file.read(),
            content_type='image/png'
        )
        # Create a Karta instance with the uploaded image
        karta = Karta(
            naziv='Test Karta',
            cena=100.0,
            opis='Opis Test Karte',
            brPrimeraka=10,
            brLajkova=5,
            brDislajkova=1,
            slika=image,
            popust=10
        )
        karta.save()

    return karta


class KartaTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_karta(self):
        karta = create_karta()
        user = create_user_with_image()
        response = self.client.get(reverse('home'))  # Testing the 'home' view
        self.assertContains(response, 'Test Karta', html=True)


class DetailsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_card_details(self):
        karta = create_karta()
        user = create_user_with_image()

        # Simulate a user clicking on the card from the home page
        response = self.client.get(reverse('card_details', args=[karta.id]))

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert that the card details are present in the response
        self.assertContains(response, 'Test Karta', html=True)

class AdministriranjeSistema_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = RegistrovanKorisnik.objects.create_superuser(
            username='admin', password='123'
        )
        self.karta = Karta.objects.create(
            naziv='Pokemon',
            cena=100,
            opis='description',
            brPrimeraka=10,
            brLajkova=0,
            brDislajkova=0,
            slika="eevee.png",
            popust=0
        )

    def test_login_uspesan(self):
        # Test if admin user can login successfully
        response = self.client.post('/admin/login/?next=/admin/', {'username': 'admin', 'password': '123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Site administration')

    def test_login_neunesen_username(self):
        # Test if admin login fails when no username is provided
        response = self.client.post('/admin/login/', {'password': '123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_login_neunesen_password(self):
        # Test if admin login fails when no password is provided
        response = self.client.post('/admin/login/', {'username': 'admin'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_login_pogresan_password(self):
        # Test if admin login fails with incorrect password
        response = self.client.post('/admin/login/', {'username': 'admin', 'password': '1234'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter the correct username and password')

    def test_login_pogresan_username(self):
        # Test if admin login fails with incorrect username
        response = self.client.post('/admin/login/', {'username': 'admin1', 'password': '123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter the correct username and password')

    def test_interfejs(self):
        self.client.login(username='admin', password='123')
        # Test access to admin interface
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Site administration')

    def test_dodavanje_karte(self):
        # Test adding a Karta object via admin
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('admin:PSI_DUCK_karta_add'), {
            'naziv': 'Pokemon',
            'cena': 50,
            'opis': 'description',
            'brPrimeraka': 5,
            'brLajkova': 0,
            'brDislajkova': 0,
            'slika': "eevee.png",
            'popust': 0
        })
        self.assertTrue(Karta.objects.filter(naziv='Pokemon').exists())

    def test_promena_karte(self):
        # Test editing a Karta object via admin
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('admin:PSI_DUCK_karta_change', args=(self.karta.id,)), {
            'naziv': 'Updated Test Card',
            'cena': 150,
            'opis': 'Updated Test Description',
            'brPrimeraka': 15,
            'brLajkova': 1,
            'brDislajkova': 0,
            'slika': "eevee.png",
            'popust': 10
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.karta.refresh_from_db()
        self.assertEqual(self.karta.naziv, 'Updated Test Card')
        self.assertEqual(self.karta.cena, 150)
        self.assertEqual(self.karta.opis, 'Updated Test Description')
        self.assertEqual(self.karta.brPrimeraka, 15)
        self.assertEqual(self.karta.brLajkova, 1)
        self.assertEqual(self.karta.popust, 10)

    def test_dodeljivanje_moderatora(self):
        self.client.login(username='admin', password='123')
        # Create a new user
        user = RegistrovanKorisnik.objects.create_user(username='test_user', password='123')

        # Create the moderator group
        moderator_group = Group.objects.create(name='moderator')

        # Assign the user to the moderator group
        user.groups.add(moderator_group)

        # Check if the user is in the moderator group
        self.assertIn(moderator_group, user.groups.all())

    def test_uklanjanje_moderatora(self):
        self.client.login(username='admin', password='123')
        # Create a new user
        user = RegistrovanKorisnik.objects.create_user(username='test_user', password='123')

        # Create the moderator group
        moderator_group = Group.objects.create(name='moderator')

        # Assign the user to the moderator group
        user.groups.add(moderator_group)

        # Create the registrovaniKorisnik group
        registrovaniKorisnik_group = Group.objects.create(name='registrovaniKorisnik')

        # Remove the user from the moderator group
        user.groups.remove(moderator_group)

        # Assign the user to the registrovaniKorisnik group
        user.groups.add(registrovaniKorisnik_group)

        # Check if the user is not in the moderator group anymore
        self.assertNotIn(moderator_group, user.groups.all())

        # Check if the user is in the registrovaniKorisnik group
        self.assertIn(registrovaniKorisnik_group, user.groups.all())

    def test_uklanjanje_naloga(self):
        # Create a new user
        user = RegistrovanKorisnik.objects.create_user(username='test_user', password='123')

        # Log in as a superuser
        self.client.login(username='admin', password='123')

        # Get the URL to remove the user account
        remove_user_url = reverse('admin:PSI_DUCK_registrovankorisnik_delete', args=[user.id])

        # Send a POST request to remove the user account
        response = self.client.post(remove_user_url, {'post': 'yes'}, follow=True)

        # Check if the user account is removed successfully
        self.assertEqual(response.status_code, 200)

        # Check if the user account is no longer in the database
        self.assertFalse(RegistrovanKorisnik.objects.filter(username='test_user').exists())


class PregledListeZelja_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = RegistrovanKorisnik.objects.create_user(username='nikola', password='milos')
        self.client.login(username='nikola', password='milos')
        self.karta = Karta.objects.create(
            naziv="Pokemon",
            brLajkova=5,
            brDislajkova=1,
            popust=0,
            brPrimeraka=20,
            slika="aaaaa",
            cena=150,
            opis="description"
        )

    def test_praznaListaZelja(self):
        response = self.client.post(reverse("wishlist"), {"wishlist_items": 0, "brkarata": 0})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your wishlist is empty!")

    def test_nepraznaListaZelja(self):
        add_to_wishlist_url = reverse("add_to_wishlist", args=[self.karta.id])
        response = self.client.post(add_to_wishlist_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ListaZelja.objects.filter(korisnik=self.user, karta=self.karta).exists())

        wishlist_url = reverse("wishlist")
        response = self.client.get(wishlist_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')

        self.assertContains(response, self.karta.naziv)
        self.assertContains(response, self.karta.opis)
        self.assertContains(response, self.karta.cena)

        self.assertEqual(response.context['brkarata'], 1)


class Sortiranje_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.karta1 = Karta.objects.create(
            naziv="Abrahadjamon",
            brLajkova=5,
            brDislajkova=10,
            popust=0,
            brPrimeraka=20,
            slika="aaaa",
            cena=50,
            opis="aaaaaaaa"
        )
        self.karta2 = Karta.objects.create(
            naziv="Brahadjamon",
            brLajkova=5,
            brDislajkova=10,
            popust=20,
            brPrimeraka=20,
            slika="bbbb",
            cena=100,
            opis="aaaaaaaa"
        )
        self.karta3 = Karta.objects.create(
            naziv="Rahadjamon",
            brLajkova=5,
            brDislajkova=10,
            popust=90,
            brPrimeraka=20,
            slika="cccc",
            cena=150,
            opis="aaaaaaaa"
        )

    def extract_card_names(self, html):
        # Extract card titles using regex
        pattern = re.compile(r'<h5 class="card-title"[^>]*>(.*?)</h5>')
        return pattern.findall(html)

    def test_ImeRastuce(self):
        response = self.client.get(reverse('fetch_cards'), {'sort_by': 'nameasc'})
        self.assertEqual(response.status_code, 200)
        karte_html = response.json()['html']
        karte_names = self.extract_card_names(karte_html)
        self.assertEqual(karte_names, ["Abrahadjamon", "Brahadjamon", "Rahadjamon"])

    def test_ImeOpadajuce(self):
        response = self.client.get(reverse('fetch_cards'), {'sort_by': 'namedesc'})
        self.assertEqual(response.status_code, 200)
        karte_html = response.json()['html']
        karte_names = self.extract_card_names(karte_html)
        self.assertEqual(karte_names, ["Rahadjamon", "Brahadjamon", "Abrahadjamon"])

    def test_CenaRastuca(self):
        response = self.client.get(reverse('fetch_cards'), {'sort_by': 'priceasc'})
        self.assertEqual(response.status_code, 200)
        karte_html = response.json()['html']
        karte_names = self.extract_card_names(karte_html)
        self.assertEqual(karte_names, ["Rahadjamon", "Abrahadjamon", "Brahadjamon"])

    def test_CenaOpadajuca(self):
        response = self.client.get(reverse('fetch_cards'), {'sort_by': 'pricedesc'})
        self.assertEqual(response.status_code, 200)
        karte_html = response.json()['html']
        karte_names = self.extract_card_names(karte_html)
        self.assertEqual(karte_names, ["Brahadjamon", "Abrahadjamon", "Rahadjamon"])
class Autorizacija_Moderatora_i_Registrovanih_KorisnikaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = RegistrovanKorisnik.objects.create_user(
            username='mihajlo', password='psiduck12345'
        )

    def test_login_uspesan(self):
        response = self.client.post('http://localhost:8000/login', {'username': 'mihajlo', 'password': 'psiduck12345'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome mihajlo!')

    def test_login_neunesen_username(self):
        # Test if admin login fails when no username is provided
        response = self.client.post('http://localhost:8000/login', {'password': 'psiduck12345'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_login_neunesen_password(self):
        # Test if admin login fails when no password is provided
        response = self.client.post('http://localhost:8000/login', {'username': 'mihajlo'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_login_pogresan_password(self):
        # Test if admin login fails with incorrect password
        response = self.client.post('http://localhost:8000/login', {'username': 'mihajlo', 'password': 'psiduck1234'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')

    def test_login_pogresan_username(self):
        # Test if admin login fails with incorrect username
        response = self.client.post('http://localhost:8000/login', {'username': 'mihajl0', 'password': 'psiduck12345'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')

    def test_redirect_na_registraciju(self):
        response = self.client.get('http://localhost:8000/login')
        register_url = reverse('register')
        self.assertContains(response, f'href="{register_url}"')

        # Simulate clicking the "Register here" link by making a GET request to the register URL
        response = self.client.get(register_url)

        # Check that the registration page is returned
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


class Registracija_KorisnikaTest(TestCase):

    def setUp(self):
        self.client = Client()
        Group.objects.create(name='registrovanKorisnik')

    def test_registracija_uspesna(self):
        url = reverse('register')

        response = self.client.post(url, data={'username': 'mihajlo2', 'password1': 'strongpassword123', 'password2': 'strongpassword123'}, follow=True)
        self.assertRedirects(response, reverse('home'))

        user_exists = RegistrovanKorisnik.objects.filter(username='mihajlo2').exists()
        self.assertTrue(user_exists)

        user = RegistrovanKorisnik.objects.get(username='mihajlo2')
        self.assertTrue(user.groups.filter(name='registrovanKorisnik').exists())

    def test_registracija_neunesen_username(self):
        url = reverse('register')

        response = self.client.post(url, data={'password1': 'strongpassword123', 'password2': 'strongpassword123'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_registracija_neunesen_password(self):
        url = reverse('register')

        response = self.client.post(url, data={'username': 'mihajlo2'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_registracija_neunesena_potvrda(self):
        url = reverse('register')

        response = self.client.post(url, data={'username': 'mihajlo2', 'password1': 'strongpassword123'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_registracija_pogresan_username(self):
        url = reverse('register')

        response = self.client.post(url, data={'username': 'mihajlo2~', 'password1': 'strongpassword123'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')

    def test_registracija_pogresan_password(self):
        url = reverse('register')

        response = self.client.post(url, data={'username': 'mihajlo2', 'password1': '123098098', 'password2': '123098098'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is entirely numeric.')

    def test_registracija_pogresna_potvrda(self):
        url = reverse('register')

        response = self.client.post(url, data={'username': 'mihajlo2', 'password1': 'mojasifra123', 'password2': 'mojasifra12'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.')

class Promena_Cene_Slicice(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = RegistrovanKorisnik.objects.create_superuser(
            username='admin', password='123'
        )
        self.client.login(username='admin', password='123')
        self.karta = Karta.objects.create(
            naziv='Pokemon',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=5,
            brDislajkova=1,
            slika="lapras.png",
            popust=0
        )

    def test_promena_cene_uspesna(self):
        url = reverse('update_card_price', args=[self.karta.id])

        new_price=150
        response = self.client.post(url, data={'new_price': new_price}, follow=True)
        self.assertRedirects(response, reverse('card_details', args=[self.karta.id]))

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.cena, new_price)

    def test_promena_cene_neuspesna_negativna(self):
        url = reverse('update_card_price', args=[self.karta.id])

        new_price = -15
        response = self.client.post(url, data={'new_price': new_price}, follow=True)
        self.assertRedirects(response, reverse('card_details', args=[self.karta.id]))

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.cena, 20)

    def test_promena_cene_neuspesna_prazna(self):
        url = reverse('update_card_price', args=[self.karta.id])

        new_price = 0
        response = self.client.post(url, data={'new_price': new_price}, follow=True)
        self.assertRedirects(response, reverse('card_details', args=[self.karta.id]))

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.cena, 20)


class Ocenjivanje_SliciceTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = RegistrovanKorisnik.objects.create_user(
            username='aca', password='psiduck12345'
        )
        self.client.login(username='aca', password='psiduck12345')
        self.karta = Karta.objects.create(
            naziv='Pokemon',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=5,
            brDislajkova=1,
            slika="groudon.png",
            popust=0
        )

    def test_lajk(self):
        url = reverse('like_card', args=[self.karta.id])

        response = self.client.get(url)

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.brLajkova, 6)

    def test_dislajk(self):
        url = reverse('dislike_card', args=[self.karta.id])

        response = self.client.get(url)

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.brDislajkova, 2)

    def test_od_lajk(self):
        url = reverse('like_card', args=[self.karta.id])

        response = self.client.get(url)
        response = self.client.get(url)

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.brLajkova, 5)

    def test_od_dislajk(self):
        url = reverse('dislike_card', args=[self.karta.id])

        response = self.client.get(url)
        response = self.client.get(url)

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.brDislajkova, 1)

class Pregled_Najpopularnijih_KarataTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.karta1 = Karta.objects.create(
            naziv='Pokemon1',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=6,
            brDislajkova=1,
            slika="groudon.png",
            popust=0
        )
        self.karta2 = Karta.objects.create(
            naziv='Pokemon2',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=5,
            brDislajkova=2,
            slika="groudon.png",
            popust=0
        )
        self.karta3 = Karta.objects.create(
            naziv='Pokemon3',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=6,
            brDislajkova=2,
            slika="groudon.png",
            popust=0
        )

    def extract_card_names(self, html):
        # Extract card titles using regex
        pattern = re.compile(r'<h5 class="card-title"[^>]*>(.*?)</h5>')
        return pattern.findall(html)

    def test_pregled(self):
        response = self.client.get(reverse('popular'))

        self.assertEqual(response.status_code, 200)

        expected_order = [self.karta1, self.karta3, self.karta2]
        self.assertQuerysetEqual(
            response.context['karte'],
            expected_order,
            transform=lambda x: x
        )

class Dodavanje_Uklanjanje_ListaZeljaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = RegistrovanKorisnik.objects.create_user(
            username='aca', password='psiduck12345'
        )
        self.client.login(username='aca', password='psiduck12345')
        self.karta1 = Karta.objects.create(
            naziv='Pokemon1',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=5,
            brDislajkova=1,
            slika="groudon.png",
            popust=0
        )
        self.karta2 = Karta.objects.create(
            naziv='Pokemon2',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=5,
            brDislajkova=2,
            slika="groudon.png",
            popust=0
        )
        self.karta3 = Karta.objects.create(
            naziv='Pokemon3',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=6,
            brDislajkova=2,
            slika="groudon.png",
            popust=0
        )
        ListaZelja.objects.create(korisnik=self.user, karta=self.karta1)

    def test_dodavanje(self):
        url = reverse('add_to_wishlist', args=[self.karta2.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ListaZelja.objects.filter(karta=self.karta2).exists())

    def test_uklanjanje(self):
        url = reverse('remove_from_wishlist', args=[self.karta1.id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ListaZelja.objects.filter(karta=self.karta1).exists())

class Dodavanje_Popusta_Na_Slicicu_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = RegistrovanKorisnik.objects.create_superuser(
            username='admin', password='123'
        )
        self.client.login(username='admin', password='123')

        self.karta = Karta.objects.create(
            naziv='Pokemon',
            cena=20,
            opis='description',
            brPrimeraka=50,
            brLajkova=5,
            brDislajkova=1,
            slika="lapras.png",
            popust=30
        )

    def test_dodavanje_popusta_uspesno(self):
        url = reverse('update_card_discount', args=[self.karta.id])

        new_discount = 10

        response = self.client.post(url, data={'new_discount': new_discount}, follow=True)
        self.assertRedirects(response, reverse('card_details', args=[self.karta.id]))

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.popust, new_discount)

    def test_dodavanje_popusta_neuspesno_negativno(self):
        url = reverse('update_card_discount', args=[self.karta.id])

        new_discount = -15
        response = self.client.post(url, data={'new_discount': new_discount}, follow=True)
        self.assertRedirects(response, reverse('card_details', args=[self.karta.id]))

        self.karta.refresh_from_db()
        self.assertEqual(self.karta.popust, 30)

class Dodavanje_I_Uklanjanje_Slicica_Test(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = RegistrovanKorisnik.objects.create_superuser(
            username='admin', password='123'
        )
        self.client.login(username='admin', password='123')

        self.karta1 = Karta.objects.create(
            naziv='Pokemon1',
            cena=20,
            opis='description',
            brPrimeraka=10,
            brLajkova=5,
            brDislajkova=1,
            slika="lapras.png",
            popust=30
        )

        self.karta2 = Karta.objects.create(
            naziv='Pokemon2',
            cena=20,
            opis='description',
            brPrimeraka=0,
            brLajkova=5,
            brDislajkova=1,
            slika="lapras.png",
            popust=30
        )

    def test_stvaranje_slicica_uspesno(self):
        image_path = os.path.join(settings.BASE_DIR, 'PSI_DUCK', 'static', 'img', 'magikarp.png')

        with open(image_path, 'rb') as image_file:
            image = SimpleUploadedFile(
                name='magikarp.png',
                content=image_file.read(),
                content_type='image/png'
            )
        url = reverse('addcard')
        karta = create_karta()
        response = self.client.post(url, data={'naziv': karta.naziv, 'opis': karta.opis, 'cena': karta.cena, 'slika': image}, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, karta.naziv)

    def test_stvaranje_slicica_neuspesno_ista_slika(self):
        url = reverse('addcard')
        karta = create_karta()
        response = self.client.post(url, data={'naziv': karta.naziv, 'opis': karta.opis, 'cena': karta.cena, 'slika': karta.slika}, follow=True)
        self.assertContains(response, "already exists")


    def test_stvaranje_slicica_neuspesno_neunesen_naziv(self):
        image_path = os.path.join(settings.BASE_DIR, 'PSI_DUCK', 'static', 'img', 'magikarp.png')

        with open(image_path, 'rb') as image_file:
            image = SimpleUploadedFile(
                name='magikarp.png',
                content=image_file.read(),
                content_type='image/png'
            )
        url = reverse('addcard')
        karta = create_karta()
        response = self.client.post(url, data={'opis': karta.opis, 'cena': karta.cena, 'slika': image}, follow=True)
        self.assertContains(response, "This field is required")


    def test_stvaranje_slicica_neuspesno_neunesen_opis(self):
        image_path = os.path.join(settings.BASE_DIR, 'PSI_DUCK', 'static', 'img', 'magikarp.png')

        with open(image_path, 'rb') as image_file:
            image = SimpleUploadedFile(
                name='magikarp.png',
                content=image_file.read(),
                content_type='image/png'
            )
        url = reverse('addcard')
        karta = create_karta()
        response = self.client.post(url, data={'naziv': karta.naziv, 'cena': karta.cena, 'slika': image}, follow=True)
        self.assertContains(response, "This field is required")

    def test_stvaranje_slicica_neuspesno_neunesena_cena(self):
        image_path = os.path.join(settings.BASE_DIR, 'PSI_DUCK', 'static', 'img', 'magikarp.png')

        with open(image_path, 'rb') as image_file:
            image = SimpleUploadedFile(
                name='magikarp.png',
                content=image_file.read(),
                content_type='image/png'
            )
        url = reverse('addcard')
        karta = create_karta()
        response = self.client.post(url, data={'naziv': karta.naziv, 'opis': karta.opis, 'slika': image}, follow=True)
        self.assertContains(response, "This field is required")


    def test_uklanjanje_slicica_uspesno(self):
        url = reverse('delete_card', args=[self.karta1.id])

        response = self.client.post(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Karta.objects.filter(id=self.karta1.id).exists())

    def test_dodavanje_instance_slicice(self):
        url = reverse('increment_karta', args=[self.karta1.id])

        response = self.client.get(url)

        self.karta1.refresh_from_db()
        self.assertEqual(self.karta1.brPrimeraka, 11)

    def test_uklanjanje_instance_slicice_uspesno(self):
        url = reverse('decrement_karta', args=[self.karta1.id])

        response = self.client.get(url)

        self.karta1.refresh_from_db()
        self.assertEqual(self.karta1.brPrimeraka, 9)

    def test_uklanjanje_instance_slicice_neuspesno(self):
        url = reverse('decrement_karta', args=[self.karta2.id])

        response = self.client.get(url)

        self.karta2.refresh_from_db()
        self.assertEqual(self.karta2.brPrimeraka, 0)


class Kupovina_Slicica_Test(TestCase):

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.brojArtikala = None

    def setUp(self):
        self.client = Client()
        self.user = RegistrovanKorisnik.objects.create_user(
            username='vuk', password='psiduck12345'
        )
        self.client.login(username='vuk', password='psiduck12345')

        self.karta = create_karta()

        self.porudzbina = InformacijePorudzbine.objects.create(
            ime='testime',
            prezime='testprezime',
            adresa='testadresa',
            grad='testgrad',
            drzava='testdrzava',
            korisnik=self.user
        )

        self.korpa = Korpa.objects.create(
            porudzbina=self.porudzbina,
            karta=self.karta,
            brojArtikala=1
        )
    def test_kupovina_slicica_uspesno(self):
        url = reverse('checkout')
        response = self.client.post(url, data={'name': self.porudzbina.ime, 'email': 'aaa@aa.com', 'address': self.porudzbina.adresa, 'city': self.porudzbina.grad, 'zip' : '11010', 'card':'123123123', 'expiry':datetime.date, 'cvv':'123'}, follow=True)

        self.assertNotContains(response, self.korpa.karta)