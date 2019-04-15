from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


import time
import datetime
import sys
import os
import pickle
import requests

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract


# Create your views here.
@csrf_exempt
def fetchresult(request, poll_id):
        pwd = os.path.dirname(__file__)
        
        r=requests.get("http://127.0.0.1:8000/polls/"+str(poll_id))
        print(r.content)
        resp=str(r.content).split('\\n')
        print("before strip")
        print(resp)
        resp=[x.strip() for x in resp]
        
        print("before after")
        print(resp)
        choices=[]
        for i in resp:
            if('label' in i):
                temp=""
                fl=0
                for j in range(1,len(i)):
                    if(i[j]=='>'):
                        fl=1
                        continue
                    if(i[j]=='<'):
                        fl=0
                    if(fl==1):
                        temp+=i[j]
                choices.append(temp)
        
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
        
        for i in range(len(choices)):
        	count_vote = contract_instance.voteCountCandidate(i)
        	num_votes.append([choices[i],count_vote])
        
        return HttpResponse(str(num_votes), content_type='text/plain')
