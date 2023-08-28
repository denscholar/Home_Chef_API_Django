from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

def create_jwt_pair_user(user:CustomUser):
    refresh = RefreshToken.for_user(user)
    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}

    return tokens
