from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import os

# Create your views here.

def getfaculty(request):

	pwd = os.path.dirname(__file__)

	with open(pwd + '/../conf/faculty.pub', 'rb') as myfile:
	  facPubKey = myfile.read()

	filename = 'faculty.pub'
	response = HttpResponse(facPubKey, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
	return response
