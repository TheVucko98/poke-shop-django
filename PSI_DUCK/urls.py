from django.urls import path

from .views import *
# Autori: Nikola Milosavljevic 0355/2021
#         Aleksandar Vuckovic  0733/2022
#         Vuk Davidovic        0705/2018
#         Mihajlo Milojevic    0317/2021


# kada dodajete u HTML, koristite "name"
# pr. href="{% url 'register' %}"
urlpatterns = [
     path('', index, name='home'),
     path('cart', cart_req, name='cart'),
     path('addcard', addcard_req, name='addcard'),
     path('deletecard<int:karta_id>', deletecard_req, name='delete_card'),
     path('confirm_delete/<int:karta_id>/', confirm_delete, name='confirm_delete'),
     path('card_details<int:karta_id>', card_details_req, name='card_details'),
     path('card_noadmin', card_noadmin_req, name='card_noadmin'),
     path('card_noregister', card_noregister_req, name='card_noregister'),
     path('checkout', checkout_req, name='checkout'),
     path('logout', logout_req, name='logout'),
     path('login', login_req, name='login'),
     path('popular', popular_req, name='popular'),
     path('purchase_history', purchase_history_req, name='purchase_history'),
     path('register', register_req, name='register'),
     path('wishlist', wishlist_req, name='wishlist'),
     path('add_to_wishlist/<int:karta_id>/', add_to_wishlist, name='add_to_wishlist'),
     path('remove_from_wishlist/<int:karta_id>/', remove_from_wishlist, name='remove_from_wishlist'),
     path('fetch_cards', fetch_cards, name='fetch_cards'),
     path('update_card_price<int:karta_id>', update_card_price, name='update_card_price'),
     path('update_card_discount<int:karta_id>', update_card_discount, name='update_card_discount'),
     path('increment_karta/<int:karta_id>/', increment_karta, name='increment_karta'),
     path('decrement_karta/<int:karta_id>/', decrement_karta, name='decrement_karta'),
     path('add_to_cart/<int:karta_id>/', add_to_cart, name='add_to_cart'),
     path('remove_from_cart/<int:karta_id>/', remove_from_cart, name='remove_from_cart'),
     path('like_card<int:karta_id>/', like_card, name='like_card'),
     path('dislike_card<int:karta_id>/', dislike_card, name='dislike_card'),
]

#python.exe ./manage.py runserver ->ZA RUNOVANJE PYTHON APLIKACIJE