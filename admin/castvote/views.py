from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pickle

import sys
import os

from web3 import Web3, HTTPProvider,eth 
from web3.contract import ConciseContract

import pickle

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
      
        http_provider = HTTPProvider('http://localhost:8545')
        eth_provider = Web3(http_provider).eth
        
        valid = verify_ring_signature(int(poll_id),hash_val, pubKeyList, *sig)
        
        msg = 'lol'
        if valid == 0:
        	msg = 'signature verification failed'
        elif valid < 0:
        	msg = 'You have already voted'
        else:
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
            
            contract_instance.commitVote(hash_val, transact=transaction_details)
            # block=(eth_provider.getBlock('latest'))['number']
            # print(block)
            
            msg = 'your vote hash has been published in blockchain'
        return HttpResponse(msg, content_type='text/plain')
