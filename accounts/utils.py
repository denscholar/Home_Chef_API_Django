from twilio.rest import Client
import random
# from django.conf import settings

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

# DENNIS
account_sid = "AC3991cbdf616298d4097cdf4a5600c57f"
auth_token = "c811100824c833d007ef2fc4fdc3849b"
client = Client(account_sid, auth_token)


def send_otp(phone_number, otp):
    message = client.messages.create(
        body=f"Your OTP verification code is: {otp}",
        from_=f"+14705163834",
        to=f"{phone_number}",
    )
    print("message sent successfully")


def generateRandomOTP(x, y):
    otp = random.randint(x, y)
    return otp
