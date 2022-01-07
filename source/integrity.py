import hashlib

def create_checksum(path:str):
    try:
        f = open(path, 'rb')
        file = f.read()
        file = bytearray(file)
        f.close()
        checksum = hashlib.sha256(file)
        f = open(path + ".chs", 'wb')
        f.write(checksum.hexdigest().encode('ascii'))
        f.close()
    except:
        print("Error creating checksum")

def check_integrity(file_path:str, chs_path:str):
    try:
        f = open(file_path, 'rb')
        file = f.read()
        file = bytearray(file)
        f.close()
        new_chs = hashlib.sha256(file)
        f = open(chs_path, 'rb')
        chs = f.readline()
        f.close()
        print(chs.decode('ascii'))
        print(new_chs.hexdigest())
        if chs.decode('ascii') == new_chs.hexdigest():
            print('Integrity check succesful.')
            return True
        else:
            print('Integrity check failed')
            return False
    except:
        print("Error checking integrity.")

if __name__ == "__main__":
    while True:
        mode = input("Enter the mode you wish :\n  -ChecksumCreate\n  -IntegrityCheck\n  -Exit\nmode >> ")
        if mode == 'ChecksumCreate':
            file_path = input("Enter the path to the desired file >> ")
            create_checksum(file_path) 
            print("Checksum created successfully.")           
        elif mode == 'IntegrityCheck':
            file_path = input("Enter the path to the desired file >> ")
            chs_path = input("Enter the path to the desired Checksum file >> ")
            check_integrity(file_path, chs_path)
        elif mode == 'Exit':
            exit(0)
        else:
            print("Please choose a valid mode.")