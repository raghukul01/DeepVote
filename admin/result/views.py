from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


import time
import datetime
import sys
import os
import pickle

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract


# Create your views here.
@csrf_exempt
def fetchresult(request, poll_id):
	pwd = os.path.dirname(__file__)

	http_provider = HTTPProvider('http://localhost:8545')
	eth_provider = Web3(http_provider).eth

	contract_abi = pickle.load(open(pwd+"/../conf/" + str(poll_id) + "contract_abi", 'rb'))
	contract_address = pickle.load(open(pwd+"/../conf/" + str(poll_id) + "contract_address", 'rb'))
	ConciseContract = pickle.load(open(pwd+"/../conf/" + str(poll_id) + "ConciseContract", 'rb'))
	
	contract_instance = eth_provider.contract(
		abi=contract_abi,
		address=contract_address,
		ContractFactoryClass=ConciseContract,
	)
	
	default_account = eth_provider.accounts[0]
	
	transaction_details = {
		'from': default_account,
	}

	contract_instance.countVotes(transact=transaction_details)
	
	num_votes = []
	
	for i in range(10):
		count_vote = contract_instance.voteCountCandidate(i)
		num_votes.append(count_vote)

	return HttpResponse(str(num_votes), content_type='text/plain')