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

	print(verify_ring_signature(hash_val, pubKeyList, *sig))
	if not verify_ring_signature(hash_val, pubKeyList, *sig):
		return HttpResponse('signature verification failed', content_type='text/plain')

	# send this to blockchain

	return HttpResponse('your vote hash has been '+
					    'published in blockchain', content_type='text/plain')