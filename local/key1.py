import os
import hashlib
import sha3
import functools
import ecdsa
import pickle
from ecdsa.util import randrange
from ecdsa.ecdsa import curve_secp256k1
from ecdsa.curves import SECP256k1
from ecdsa import numbertheory
from ecdsa import SigningKey


with open("faculty.pub","rb") as f:
    facultylist=pickle.load(f)
facultylist=[x[1] for x in facultylist]

open('pubkey',"wb").write(pickle.dumps(facultylist[0]))
