import hashlib 
import binascii
import sys
vote=sys.argv[1]
nonce=sys.argv[2]
pollNo=sys.argv[3]

strnonce = str(nonce)
vote = int(vote)
nonce = strnonce.encode().hex()
hexvote = hex(vote)[2:]
if (vote < 16):
    hexvote = '0' + hexvote
s = '0x' + nonce + hexvote 
d = '0x' + hashlib.sha256(binascii.unhexlify(s[2:])).hexdigest()

f=open(pollNo+"datahash.txt",'w')
f.write(d)
f.close()
