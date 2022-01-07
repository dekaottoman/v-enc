def encryption(path: str, key: str):
    try:        
        key = list(key)

        f = open(path, 'rb')
        file = f.read()
        f.close()

        file = bytearray(file)
        for index, values in enumerate(file):
            file[index] = values ^ ord(key[index%len(key)])
    
        f = open(path + ".enc", 'wb')
        f.write(file)
        f.close()
        print('Encryption Done...')
    except:
        print("An Error has occured.")
    
def decryption(path: str, key: str):
    try:
        key = list(key)

        f = open(path, 'rb')
        file = f.read()
        f.close()

        file = bytearray(file)
        for index, values in enumerate(file):
            file[index] = values ^ ord(key[index%len(key)])
    
        f = open(path.replace(".enc", ""), 'wb')
        f.write(file)
        f.close()
        print('Decryption Done...')
    except:
        print("An Error has occured.")
    

if __name__ == "__main__":
    while True:
        mode = input("Enter the mode you wish :\n  -Encryption\n  -Decryption\n  -Exit\nmode >> ")
        if(mode == "Encryption"):
            path = input("Enter path to file that you wish to encrypt >> ")
            key = input("Enter the key for the encryption >> ")
            encryption(path, key)
        elif(mode == "Decryption"):
            path = input("Enter path to file that you wish to decrypt >> ")
            key = input("Enter the key for the decryption >> ")
            decryption(path, key)
        elif(mode == "Exit"):
            exit(0)
        else:
            print("Please choose a valid mode.")