from django.urls import path
from .views import SignIn, SignUp
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('sign_in/', SignIn.as_view(), name='sign_in'),
    path('sign_out/', LogoutView.as_view(next_page='index'), name='sign_out'),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
]

