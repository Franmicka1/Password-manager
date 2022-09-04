import sys
import os
import struct
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

BUFFER_SIZE = 1024 * 1024
ENK_DAT = "pass.encrypted"


def encrypt_init(master_pass):
    output_filename = ENK_DAT 

    file_out = open(output_filename, 'wb')  

    salt = get_random_bytes(32) 
    key = scrypt(master_pass, salt, key_len=32, N=2**17, r=8, p=1)  
    file_out.write(salt)  

    cipher = AES.new(key, AES.MODE_GCM)  
    file_out.write(cipher.nonce)  

    tag = cipher.digest()  
    file_out.write(tag)

    file_out.close()
    return 0

def encrypt(master_pass, podatci): 
    output_filename = ENK_DAT

    file_out = open(output_filename, 'wb')

    salt = get_random_bytes(32) 
    key = scrypt(master_pass, salt, key_len=32, N=2**17, r=8, p=1)  
    file_out.write(salt)  

    cipher = AES.new(key, AES.MODE_GCM)  
    file_out.write(cipher.nonce)
    
    encrypted_data = cipher.encrypt(podatci.encode())
    file_out.write(encrypted_data)
    
    tag = cipher.digest()  
    file_out.write(tag)

    
    file_out.close()
    return 0


def decrypt(master_pass):
    
    input_filename = ENK_DAT 
    var = ""

    file_in = open(input_filename, 'rb')

    salt = file_in.read(32)
    key = scrypt(master_pass, salt, key_len=32, N=2**17, r=8, p=1) 

    nonce = file_in.read(16)  
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    file_in_size = os.path.getsize(input_filename)
    encrypted_data_size = file_in_size - 32 - 16 - 16  

    for _ in range(int(encrypted_data_size / BUFFER_SIZE)):  
        data = file_in.read(BUFFER_SIZE)  
        decrypted_data = cipher.decrypt(data)
        try:
            var+= decrypted_data.decode("utf-8")  
        except:
            print("Master password incorrect or integrity check failed.")
            return 1
    data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))  
    decrypted_data = cipher.decrypt(data)  
    try:
        var+= decrypted_data.decode("utf-8")  
    except:
        print("Master password incorrect or integrity check failed.")
        return 1
    
    tag = file_in.read(16)
    try:
        cipher.verify(tag)
    except ValueError as e:
        
        file_in.close()
        print("Master password incorrect or integrity check failed.")
        return 1
   
    file_in.close()
    
    return var


n = len(sys.argv)
for i in range(1, n):
     
    if("init" in sys.argv[i]):
        i+=1
        try:
            master_pass = sys.argv[i]
        except:
            print("Krivo uneseni argumenti za init metodu.")
            os._exit(0)
        
        encrypt_init(master_pass)
        print("Password manager initialized.")

    if("put" in sys.argv[i]):
        i+=1
        try:
            master_pass = sys.argv[i]
            adresa = sys.argv[i+1]
            zaporka = sys.argv[i+2]
        except:
            print("Krivo uneseni argumenti za put metodu.")
            os._exit(0)
        
        podatci = decrypt(master_pass) 
        #pohrani novo u dat

        if podatci==1:
            os._exit(0)
        
        z=0
        if podatci:
            list_pod=podatci.strip()
            list_pod=list_pod.split("|")
            podatci=""
            for j in range(len(list_pod)):
                tr=list_pod[j].split(":")
                if tr[0]==adresa:
                    z=1
                    tr[1]=zaporka
                    str_tr = tr[0]+":"+tr[1]
                    list_pod[j] = str_tr
                    print("Changed password for "+ adresa)
                if list_pod[j]!='':
                    podatci+=list_pod[j]+"|"
               

        if z==0:
            podatci+=adresa+":"+zaporka+"|"
            print("Stored password for "+ adresa)
            
        encrypt(master_pass, podatci)
        
    if("get" in sys.argv[i]):
        i+=1
        try:
            master_pass = sys.argv[i]
            adresa = sys.argv[i+1]
            
        except:
            print("Krivo uneseni argumenti za get metodu.")
            os._exit(0)
            
        podatci = decrypt(master_pass)
        z=0
        #dohvati podatak
        if podatci==1:
            os._exit(0)
        
        if podatci:
            list_pod=podatci.strip()
            list_pod=list_pod.split("|")
            for j in range(len(list_pod)):
                tr=list_pod[j].split(":")
                if tr[0]==adresa:
                    z=1
                    print("Password for "+ tr[0] +" is: "+ tr[1])
        

        if z==0:
            print("No password for adress " + adresa)
            
            
        
            
