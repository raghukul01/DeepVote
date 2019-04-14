import os,sys,requests,pickle

pollNo=sys.argv[1]

vote = str(open(pollNo+'vote.txt','r').read().strip())
nonce = str(open(pollNo+'nonce.txt','r').read().strip())

r = requests.get('http://127.0.0.1:8000/reveal/'\
                           +pollNo+'/'+nonce+'/'+vote)
print(r.content)

