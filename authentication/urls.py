from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import  Registerview, ProfileView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view()),
    path("register/", Registerview.as_view()),
    path("me/", ProfileView.as_view()),
#    path("rest-auth/", include("rest_auth.urls")),
#    path("rest-auth/registration/", include("rest_auth.registration.urls")),
#    path("rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
#    path(r"^accounts/", include("allauth.urls"), name="socialaccount_signup"),
]
