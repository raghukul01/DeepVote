import pickle
import ecdsa
pubs=pickle.load(open('faculty.pub','rb'))
prvs=pickle.load(open('faculty.prv','rb'))

for i in range(len(pubs)):
    with open ("pubkey_"+ str(i), 'wb') as handle:
        pickle.dump(pubs[i], handle, protocol=3)
    with open ("prvkey_"+ str(i), 'wb') as handle:
        pickle.dump(prvs[i], handle, protocol=3)

        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
	
	
	
	
