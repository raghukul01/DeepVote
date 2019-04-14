from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pickle

import sys
import os

sys.path.append(os.path.abspath('..'))

from linkable_ring_signature import verify_ring_signature 

# Create your views here.

@csrf_exempt
def castvote(request, poll_id, hash_val):
	sigFile = request.FILES['sig_dump']

	pwd = os.path.dirname(__file__)

	facPubKeys = pickle.load(open(pwd+'/../conf/faculty.pub', 'rb'))
	sig = pickle.load(sigFile)

	pubKeyList = [facPubKeys[i][1] for i in range(len(facPubKeys))]


	valid = verify_ring_signature(hash_val, pubKeyList, *sig)

	msg = 'lol'
	if valid == 0:
		msg = 'signature verification failed'
	elif valid < 0:
		msg = 'You have already voted'
	else:
		msg = 'your vote hash has been published in blockchain'
	return HttpResponse(msg, content_type='text/plain')
