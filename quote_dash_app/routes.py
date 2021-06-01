from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotes),
    path('logout', views.logout),
    path('quote_add', views.quote_add),
    path('myaccount/<int:user_id>', views.edit_account),
    path('update_account/<int:user_id>', views.update_account),
    path('user_quotes/<int:user_id>', views.user_quotes),
    path('quote/delete/<int:quote_id>', views.delete)
]