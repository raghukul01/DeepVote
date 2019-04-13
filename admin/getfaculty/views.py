from django.shortcuts import render, render_to_response
import csv
from django.http import HttpResponse
import os

# Create your views here.

def getfaculty(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="faculty.csv"'

	writer = csv.writer(response)

	# read the config file

	pwd = os.path.dirname(__file__)

	with open(pwd + '/../conf/faculty.csv') as facultyCSV:
		csvReader = csv.reader(facultyCSV, delimiter=',')
		for row in csvReader:
			print(row)
			writer.writerow(row)

	return response
