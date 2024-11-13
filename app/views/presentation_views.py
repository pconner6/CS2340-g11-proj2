import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from datetime import datetime

def presentation(request):
    return render(request, 'app/presentation.html')