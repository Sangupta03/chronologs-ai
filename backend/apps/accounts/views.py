
# Create your views here.

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class ProtectedTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})
