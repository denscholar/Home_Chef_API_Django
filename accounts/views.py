from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import SignUpUserSerializer


# sign_up
class SignUpView(APIView):
    serializer_class = SignUpUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response = {"message": "user successfully created", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
