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

sk = [randrange(SECP256k1.order)]
vk = map(lambda xi: SECP256k1.generator * xi, sk)
open("privkey","wb").write(str(sk[0]))
open("pubkey","wb").write(pickle.dumps(vk))
