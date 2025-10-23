# svi studenti su odgovorni za ovaj fajl
# Autori: Nikola Milosavljevic 0355/2021
#         Aleksandar Vuckovic  0733/2022
#         Vuk Davidovic        0705/2018
#         Mihajlo Milojevic    0317/2021

from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from django.shortcuts import redirect

from django.http import Http404

from prvi_Pokusaj import settings
from .forms import *
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.models import Group
from .utils import *
from django.utils import timezone


# Create your views here.
def index(request: HttpRequest):
    """
        Show all cards on site.

        **Context**

        ``karte``
            array of  Cards.

        **Template:**

        :template:`index.html + base.html`
    """
    karte = Karta.objects.all()
    cart_items_count = 0
    if request.user.is_authenticated:
        order_info, created = InformacijePorudzbine.objects.get_or_create(
            korisnik=request.user,
            defaults={'datum': timezone.now()}
        )
        cart_items_count = \
        Korpa.objects.filter(porudzbina=order_info).aggregate(total_items=models.Sum('brojArtikala'))[
            'total_items'] or 0

    context = {
        'karte': karte,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'index.html', context)


from django.http import JsonResponse
from django.template.loader import render_to_string


def fetch_cards(request):
    """
           Ajax will call this function.
           To periodically fetch cards from Karte.

           **Context**

           ``karte``
               array of  Cards.

           **Template:**

           :template:`cards_partial.html`
       """

    karte = vratiSortiraneKartePoParametruIzOpcije(request)

    context = {'karte': karte}
    html = render_to_string('cards_partial.html', context)
    return JsonResponse({'html': html})


import urllib.parse  # Da bih znao sa koje stranice je kliknut Lajk/Dislajk


@login_required(login_url='login')
def like_card(request, karta_id):
    """
            Increments the rating of the card, if clicked twice the action is reversed.

            **Context**

            **Template:**

            :template:`popular.html, wishlist.html, index.html`
        """
    karta = Karta.objects.get(pk=karta_id)
    korisnik = request.user

    ocenio, created = jeOcenio.objects.get_or_create(korisnik=korisnik, karta=karta)

    if ocenio.ocena == 1:
        karta.brLajkova -= 1
        ocenio.ocena = 0
    else:
        if ocenio.ocena == -1:
            karta.brDislajkova -= 1
        karta.brLajkova += 1
        ocenio.ocena = 1

    karta.save()
    ocenio.save()

    referer = request.META.get('HTTP_REFERER', '')

    # Parse the referer URL
    parsed_url = urllib.parse.urlparse(referer)

    if '/popular' in referer:
        return redirect('popular')
    elif '/wishlist' in referer:
        return redirect('wishlist')
    else:
        return redirect('home')


@login_required(login_url='login')
def dislike_card(request, karta_id):
    """
            Decrements the rating of the card, if clicked twice the action is reversed.

            **Context**

            **Template:**

            :template:`popular.html, wishlist.html, index.html`
        """
    karta = Karta.objects.get(pk=karta_id)
    korisnik = request.user

    ocenio, created = jeOcenio.objects.get_or_create(korisnik=korisnik, karta=karta)

    if ocenio.ocena == -1:
        karta.brDislajkova -= 1
        ocenio.ocena = 0
    else:
        if ocenio.ocena == 1:
            karta.brLajkova -= 1
        karta.brDislajkova += 1
        ocenio.ocena = -1

    karta.save()
    ocenio.save()

    referer = request.META.get('HTTP_REFERER', '')

    # Parse the referer URL
    parsed_url = urllib.parse.urlparse(referer)

    if '/popular' in referer:
        return redirect('popular')
    elif '/wishlist' in referer:
        return redirect('wishlist')
    else:
        return redirect('home')


@login_required(login_url='login')
@permission_required('psi_duck.add_karta', raise_exception=True)
def addcard_req(request: HttpRequest):
    """
               Returns a request to add cards to Karte.

               **Context**

               ``form``
                   A form for adding new cards.

               **Template:**

               :template:`addcard.html`
           """
    form2 = KartaCreationForm(request.POST, request.FILES)

    if form2.is_valid():
        slikaUrl = form2.cleaned_data['slika'].name
        slikaUrl = 'imgs/' + slikaUrl
        if Karta.objects.filter(slika=slikaUrl).exists():
            form2.add_error('slika', 'A card with this image already exists.')
        else:
            form2.save()
            return redirect('home')
        # Izbacio sam proveru originalnosti slicice
        # Jer mi i zelimo vise primeraka istog pokemona, sa razlicitim cenamaa je takodje dozvoljeno
        # i opisom

    context = {
        'form': form2,
    }
    return render(request, 'addcard.html', context)


import os


@login_required(login_url='login')
@permission_required('psi_duck.delete_karta', raise_exception=True)
def deletecard_req(request: HttpRequest, karta_id):
    """
                   Returns a request to remove cards from Karte.

                   **Context**

                   **Template:**

                   :template:`index.html`
               """
    karta = get_object_or_404(Karta, pk=karta_id)

    if request.method == 'POST':

        if karta.slika:
            image_path = os.path.join(settings.MEDIA_ROOT, karta.slika.name)

        print(image_path)
        karta.delete()
        #Obrisi sliku iz media
        if karta.slika and os.path.exists(image_path):
            os.remove(image_path)

        return redirect('home')


@login_required(login_url='login')
@permission_required('psi_duck.delete_karta', raise_exception=True)
def confirm_delete(request: HttpRequest, karta_id):
    """
                Returns a request to delete cards from Karte.

               **Context**

               ``slikaUrl``
                    url of karta
               ``form``
                    form for deleting cards from Karte.
               ``karta``
                    array of Karta objects.

               **Template:**

               :template:`confirm_delete.html`
    """
    karta = get_object_or_404(Karta, pk=karta_id)
    form = ConfirmDeleteForm()
    slikaUrl = karta.slika.url

    return render(request, 'confirm_delete.html', {'slikaUrl': slikaUrl, 'form': form, 'karta': karta})


@login_required(login_url='login')
@permission_required('PSI_DUCK.change_karta')
def increment_karta(request, karta_id):
    """
               Increments the number of available cards

               **Context**

               **Template:**

               :template:`card_details.html`
    """
    karta = get_object_or_404(Karta, id=karta_id)
    karta.brPrimeraka += 1
    karta.save()
    return redirect('card_details', karta_id)


@login_required(login_url='login')
@permission_required('PSI_DUCK.change_karta')
def decrement_karta(request, karta_id):
    """
               Decrements the number of available cards

               **Context**

               **Template:**

               :template:`card_details.html`
    """
    karta = get_object_or_404(Karta, id=karta_id)
    if karta.brPrimeraka > 0:
        karta.brPrimeraka -= 1
        karta.save()
    return redirect('card_details', karta_id)


def card_details_req(request: HttpRequest, karta_id):
    """
               Shows details of a selected card

               **Context**

               ``karta``
                   a Karta object.
               ``slikaUrl``
                    url of karta

               **Template:**

               :template:`card_details.html`
    """
    karta = Karta.objects.get(pk=karta_id)
    slikaUrl = karta.slika.url
    context = {
        'karta': karta,
        'slikaUrl': slikaUrl,
    }
    return render(request, 'card_details.html', context)


def add_to_cart(request, karta_id):
    """
                   Adds a new card to the cart

                   **Context**
                    ``karta``
                   a Karta object.
                    ``slikaUrl``
                    url of karta
                   **Template:**

                   :template:`card_details.html`
        """
    karta = get_object_or_404(Karta, pk=karta_id)
    order_info, created = InformacijePorudzbine.objects.get_or_create(
        korisnik=request.user,
        defaults={
            'datum': datetime.date.today(),
            'ime': request.user.first_name,
            'prezime': request.user.last_name,
            'adresa': 'Default Address',  # Update with actual address if available
            'grad': 'Default City',
            'drzava': 'Default Country'
        }
    )

    cart_item, created = Korpa.objects.get_or_create(porudzbina=order_info, karta=karta)
    if not created:
        cart_item.brojArtikala += 1
    else:
        cart_item.brojArtikala = 1
    cart_item.save()

    karta.brPrimeraka -= 1
    karta.save()

    slikaUrl = karta.slika.url
    context = {
        'karta': karta,
        'slikaUrl': slikaUrl,
    }
    return render(request, 'card_details.html', context)


@login_required(login_url='login')
def remove_from_cart(request, karta_id):
    """
                       Removes a card from the cart

                       **Context**

                       **Template:**

                       :template:`cart.html`
            """
    karta = get_object_or_404(Karta, pk=karta_id)
    order_info = get_object_or_404(InformacijePorudzbine, korisnik=request.user)
    cart_item = get_object_or_404(Korpa, porudzbina=order_info, karta=karta)

    if cart_item.brojArtikala > 1:
        cart_item.brojArtikala -= 1
        cart_item.save()
    else:
        cart_item.delete()

    # Increase the available quantity of the card
    karta.brPrimeraka += 1
    karta.save()

    return redirect('cart')


@login_required(login_url='login')
def cart_req(request):
    """
                          Views the cart

                          **Context**
                            ``cart_items``
                                an array of cart items.
                            ``total_price``
                                total price of all cards in the cart
                            ``total_items``
                                total number of cards in the cart
                          **Template:**

                          :template:`cart.html`
               """
    order_info, created = InformacijePorudzbine.objects.get_or_create(korisnik=request.user)
    cart_items = Korpa.objects.filter(porudzbina=order_info)
    for item in cart_items:
        item.total_price = item.brojArtikala * item.karta.cena_sa_popustom()
    total_price = sum(item.brojArtikala * item.karta.cena_sa_popustom() for item in cart_items)
    total_items = sum(item.brojArtikala for item in cart_items)
    print(total_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
    }
    return render(request, 'cart.html', context)


@login_required(login_url='login')
def checkout_req(request: HttpRequest):
    """
                              Views the checkout page

                              **Context**
                                ``form``
                                    a form for filling the customer info.
                                ``total_price``
                                    total price of all cards in the cart
                                ``cart_items``
                                    an array of cart items.
                              **Template:**

                              :template:`checkout.html`
                   """
    order_info, created = InformacijePorudzbine.objects.get_or_create(korisnik=request.user)
    cart_items = Korpa.objects.filter(porudzbina=order_info)
    for item in cart_items:
        item.price = item.brojArtikala * item.karta.cena_sa_popustom()
    total_price = sum(item.price for item in cart_items)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            for item in cart_items:
                IstorijaKupovine.objects.create(
                    korisnik=request.user,
                    karta=item.karta,
                    kolicina=item.brojArtikala,
                    datum=timezone.now().date(),
                    vreme=timezone.now().time()
                )
            # Process the form data
            # Save the order information or perform any other necessary action
            cart_items.delete()
            return redirect('home')  # Redirect to a success page
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def purchase_history_req(request):
    """
                                  Views the purchase history page

                                  **Context**
                                    ``purchase_history``
                                        an array of all purchase history items.
                                  **Template:**

                                  :template:`purchase_history.html`
                       """
    purchase_history = IstorijaKupovine.objects.filter(korisnik=request.user)
    total_price = 0
    for item in purchase_history:
        item.total_price = (item.karta.cena_sa_popustom() * item.kolicina)
    context = {
        'purchase_history': purchase_history,
    }
    return render(request, 'purchase_history.html', context)


@login_required(login_url='login')
@permission_required('PSI_DUCK.change_karta')
def update_card_price(request: HttpRequest, karta_id):
    """
               Updates the price of a card

               **Context**

               **Template:**

               :template:`cards_details.html`
    """
    karta = get_object_or_404(Karta, pk=karta_id)

    if request.method == 'POST':
        new_price = request.POST.get('new_price')
        if float(new_price) > 0:
            karta.cena = new_price
            karta.save()
        return redirect('card_details', karta_id=karta_id)


@login_required(login_url='login')
@permission_required('PSI_DUCK.change_karta')
def update_card_discount(request: HttpRequest, karta_id):
    """
               Updates the discount of a card

               **Context**

               **Template:**

               :template:`cards_details.html`
    """
    karta = get_object_or_404(Karta, pk=karta_id)

    if request.method == 'POST':
        new_discount = request.POST.get('new_discount')
        if 100 > float(new_discount) > 0:
            karta.popust = new_discount
            karta.save()
        return redirect('card_details', karta_id=karta_id)


def card_noadmin_req(request: HttpRequest):
    """
                   Views the card page while the user is a non-admin

                   **Context**

                   **Template:**

                   :template:`card_noadmin.html`
        """
    return render(request, 'card_noadmin.html', {})


def card_noregister_req(request: HttpRequest):
    """
                       Views the card page while the user is a non-registered user

                       **Context**

                       **Template:**

                       :template:`card_noregister.html`
            """
    return render(request, 'card_noregister.html', {})


def logout_req(request: HttpRequest):
    """
                       Logs out the user

                       **Context**

                       **Template:**

                       :template:`index.html`
            """
    logout(request)

    return redirect('home')


def login_req(request: HttpRequest):
    """
                   User login page

                   **Context**
                        ``form``
                        a form for filling the user login.
                   **Template:**

                   :template:`login.html + index.html`
        """
    if request.user.is_authenticated:  # Ako je ulogovan, skoci na home
        return redirect('home')

    form = LoginKorisnikForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # On gleda nas onaj autentication sto smo pravili, koji je samo extraxtovan ali isto radi kao defualtni
            user = authenticate(username=username, password=password)
            if user:
                # Obrati paznju da on ubacu  seasion storage user-a
                login(request, user)

                # Poruka
                messages.info(request, 'Welcome ' + username + '!')

                # Obrati paznju ovde, idemo preko "imena f-je" ne preko "index ili index.html ili /"
                return redirect('home')
        else:
            messages.info(request, "Failed to login")

    context = {
        'form': form
    }

    return render(request, 'login.html', context)


def popular_req(request: HttpRequest):
    """
                       Views the most popular cards page

                       **Context**
                            ``karte``
                                an array of cards.
                            ``cart_items_count``
                                the total number of cards in the cart.

                       **Template:**

                       :template:`popular.html`
            """
    karte = Karta.objects.all().order_by('-brLajkova', 'brDislajkova')

    cart_items_count = 0
    if request.user.is_authenticated:
        order_info, created = InformacijePorudzbine.objects.get_or_create(
            korisnik=request.user,
            defaults={'datum': timezone.now()}
        )
        cart_items_count = \
            Korpa.objects.filter(porudzbina=order_info).aggregate(total_items=models.Sum('brojArtikala'))[
                'total_items'] or 0

    context = {
        'karte': karte,
        'cart_items_count' : cart_items_count
    }

    return render(request, 'popular.html', context)


def register_req(request: HttpRequest):
    """
                   User register page

                   **Context**
                        ``form``
                        a form for filling the user register
                   **Template:**

                   :template:`register.html + index.html`
        """
    form = KorisnikCreationForm(request.POST, request.FILES)

    if form.is_valid():
        #Ono cudo extenduje formu, pa ovo zato mozemo da uradimo
        user: RegistrovanKorisnik = form.save()  # :Korisnik,  da bi imao autocomplete
        # Da uradimo update ovde ?
        group = Group.objects.get(name='registrovanKorisnik')
        user.groups.add(group)
        #
        login(request, user)
        # Obrati paznju ovde, idemo preko "imena f-je" ne preko "index ili index.html ili /"
        return redirect('home')
    if request.method != 'POST':  # Ako nismo Register kliknuli, napravi praznu formu
        # Ovo sam radio, jer mi inace izbacije dosta vise info " tipa this field is required" itd
        form = KorisnikCreationForm(None)
    context = {
        'form': form
    }

    return render(request, 'register.html', context)


@login_required(login_url='login')
def wishlist_req(request: HttpRequest):
    """
                       Views the wishlist page

                       **Context**
                            ``wishlist_items``
                            an array of cards in the wishlist.
                            ``brkarata``
                            number of cards in the wishlist.
                       **Template:**

                       :template:`wishlist.html`
            """
    wishlist_items = ListaZelja.objects.filter(korisnik=request.user)

    brkarata=len(wishlist_items)

    context = {
        'wishlist_items': wishlist_items,
        'brkarata': brkarata
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='login')
def add_to_wishlist(request, karta_id):
    """
                           Adds a card to the wishlist

                           **Context**
                                ``karta``
                                    a card
                                ``slikaurl``
                                    the url of the card
                           **Template:**

                           :template:`index.html`
                """
    if request.method == 'POST':

        karta = get_object_or_404(Karta, pk=karta_id)

        wishlist_item, created = ListaZelja.objects.get_or_create(
            korisnik=request.user,
            karta=karta
        )

        slikaurl = karta.slika.url
        context = {
            'karta': karta,
            'slikaurl': slikaurl
        }
        return render(request, 'index.html', context)
    return redirect("home")

@login_required(login_url='login')
def remove_from_wishlist(request, karta_id):
    """
                               Removes a card from the wishlist

                               **Context**

                               **Template:**

                               :template:`wishlist.html`
                    """
    karta = get_object_or_404(Karta, pk=karta_id)

    wishlist_item = get_object_or_404(ListaZelja, korisnik=request.user, karta=karta)
    wishlist_item.delete()

    return redirect('wishlist')

