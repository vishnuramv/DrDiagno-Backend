from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
#from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
#from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
#from rest_auth.registration.views import SocialLoginView

from .models import Profile
from .serializer import ProfileSerailizer

User = get_user_model()


#class GoogleLogin(SocialLoginView):
 #   adapter_class = GoogleOAuth2Adapter


class Registerview(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        image = request.data.get("image")
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        age = request.data.get("age")
        gender = request.data.get("gender")
        bloodgroup = request.data.get("bloodgroup")

        print([email, username, password, age, gender, bloodgroup, image])

        if not all([email, username, password, age, gender, bloodgroup, image]):
            return Response(
                {"error": "credentials not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"type": "EMAIL", "error": "email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.create_user(
                email=email,
                # mocking the email as username
                username=email,
                password=password,
            )
            user.save()

            profile = Profile()
            profile.user = user
            profile.username = username
            profile.age = age
            profile.gender = gender
            profile.bloodgroup = bloodgroup
            profile.profile_pic = image
            profile.save()
            return Response(
                {"msg": "User created successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProfileView(APIView):
    def get(self, request):
        user = request.user

        profile = Profile.objects.filter(user=user)[0]
        serialized = ProfileSerailizer(profile)

        return Response(serialized.data)
