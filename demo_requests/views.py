from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from .models import DemoRequest
from .serializers import DemoRequestSerializer


class DemoRequestCreateView(generics.CreateAPIView):
    queryset = DemoRequest.objects.all()
    serializer_class = DemoRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "demo_request"