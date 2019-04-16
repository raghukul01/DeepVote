import os,sys,requests,pickle
from web3 import Web3, HTTPProvider,eth 
from web3.contract import ConciseContract

pollNo=sys.argv[1]

http_provider = HTTPProvider('http://localhost:8545')
eth_provider = Web3(http_provider).eth

vote = str(open(pollNo+'vote.txt','r').read().strip())
nonce = str(open(pollNo+'nonce.txt','r').read().strip())

r = requests.get('http://127.0.0.1:8000/reveal/'\
                           +pollNo+'/'+nonce+'/'+vote)
print(r.content)

block=(eth_provider.getBlock('latest'))['number']

with open(str(pollNo)+'BlockReveal.txt','w') as f:
    f.write(str(block))
f.close()
