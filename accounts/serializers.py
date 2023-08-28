from rest_framework import serializers
from .models import CustomUser
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .utils import send_otp, generateRandomOTP


class SignUpUserSerializer(serializers.ModelSerializer):
    """
    This code defines two CharField attributes for the password1 and password2 fields, respectively. These fields are write-only and have a minimum length of settings.MIN_PASSWORD_LENGTH. If the password entered by the user is shorter than settings.MIN_PASSWORD_LENGTH, an error message is returned.
    """

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email_address = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=14, required=True)
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "password must be longer than {settings.MIN_PASSWORD_LENGTH} characters".format(
                settings=settings
            )
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "password must be longer than {settings.MIN_PASSWORD_LENGTH} characters".format(
                settings=settings
            )
        },
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email_address",
            "phone_number",
            "password1",
            "password2",
        )

    def validate(self, data):
        phone_number = data.get("phone_number")
        
        print(phone_number)

        # validate phone number to check if it exist in database
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"errors": f"User with the phone number {phone_number} already exists"}
            )

        # validate password to ensure they are the same password
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Password do not match")
        if len(data["password1"]) < settings.MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(
                "Password must be at least {settings.MIN_PASSWORD_LENGTH} characters long.".format(
                    settings=settings
                )
            )

        # handle the phone number with and without +234
        if len(phone_number) == 11:
            phone_number = "+234" + phone_number[1:]
        elif len(phone_number) == 13:
            phone_number = "+" + phone_number
        elif len(phone_number) == 14:
            pass
        else:
            raise serializers.ValidationError(
                {"error": "Phone number must start with '+234' or '080' "}
            )
        data["phone_number"] = phone_number
        return data

    """You will need to hash the passowrd and to do that, you will need to overide the create method. The create method is one that will run each time we call the .save method. so we are going to overide that and dictate how we will save the data in the database."""

    def create(self, validated_data):
        # access the validated phone_number and password1
        passwords = validated_data.pop("password1", None)
        validated_data.pop("password2", None)
        user = super().create(validated_data)
        user.set_password(passwords)

        # Saves the user to the database
        user.save()

        # create a token for this specific user that signs up
        Token.objects.create(user=user)

        # send OTP to validate the user
        otp = generateRandomOTP(100000, 999999)
        send_otp(phone_number=user.phone_number, otp=otp)


        response_message = f"An OTP has been sent to this phone number {user.phone_number}."
        return Response({"message": response_message})
