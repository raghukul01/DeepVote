from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def castvote(request):
	file = request.FILES['a']
	print(file.read())
	return HttpResponse('')