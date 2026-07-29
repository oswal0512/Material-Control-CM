from django.urls import path
from django.contrib.auth.views import LoginView
from .views import logout_view

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),
]