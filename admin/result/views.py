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
        Question=""
        for i in resp:
            if('h1' in i):
                fl=0
                for j in range(1,len(i)):
                    if(i[j]=='>'):
                        fl=1
                        continue
                    if(i[j]=='<'):
                        fl=0
                    if(fl==1):
                        Question+=i[j]
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
        result = "<html><head><title>Poll Result</title><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css\"><style> body { background-color: #ECEFF1; font-family: Helvetica; } .receipt { width: 400px; background-color: transparent; margin: 80px auto 80px auto; } .table-receipt { border-radius: 10px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; width: 100%; border-collapse: collapse; box-shadow: -20px 30px 50px 0px #8d8d8d; background-color: white; } .th-header { border-top-left-radius: 10px; border-top-right-radius: 10px; width: 100%; background-color: #3a903e; color: white; padding: 24px; font-size: 24px; } .td-title { font-size: 16px; font-weight: 700; color: #78909c; padding: 12px 8px 12px 8px; border-bottom: 1px solid #CFD8DC; } .td-content { font-size: 18px; text-align: right; padding: 12px 8px 12px 8px; border-bottom: 1px solid #CFD8DC; } .td-bottom { width: 100%; font-weight: 600; color: #3a903e; text-align: center; padding: 24px; font-size: 20px; } </style></head><body style=\"text-align:center;background-color: #7bdcf4;\"><div class=\"container\" style=\"width:250px;height:1000px;margin:30px auto;\" ><table><thead><tr><th class=\"th-header\"colspan=\"2\">"+Question+"</th></tr></thead><tbody style=\"background-color:#FFFFFF\">"
        num_votes = []
        
        result+="<tr><td class=\"td-title\">"
        result+="Options"
        result+="</td><td class=\"td-content\">"
        result+="Votes"
        result+="</td></tr>"
        for i in range(len(choices)):
            count_vote = contract_instance.voteCountCandidate(i)
            result+="<tr><td class=\"td-title\">"
            result+=str(choices[i])
            result+="</td><td class=\"td-content\">"
            result+=str(count_vote)
            result+="</td></tr>"
            # num_votes.append([choices[i],count_vote])
        result+="</tbody></table></div></body></html>"
        
        return HttpResponse(result, content_type='text/html') 
        # num_votes = []
        
        # for i in range(len(choices)):
        # 	count_vote = contract_instance.voteCountCandidate(i)
        # 	num_votes.append([choices[i],count_vote])
        
        # return HttpResponse(str(num_votes), content_type='text/plain')
