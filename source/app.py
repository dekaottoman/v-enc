import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import hashlib
import os
import qrcode
import cv2

root = tk.Tk()
root.maxsize(300,600)
root.minsize(300,600)
root.title('V Enc')
icon = tk.PhotoImage("icon.ico")
root.iconbitmap(icon)


if os.name == "nt":
    downloads = f"{os.getenv('USERPROFILE')}\\Downloads"
else:
    downloads = f"{os.getenv('HOME')}/Downloads"

def pop_up(msg:str):
    win = tk.Toplevel()
    win.wm_title("For you!")
    win.maxsize(243,150)
    win.minsize(243,150)
    win.iconbitmap(icon)

    l = tk.Label(win, text=msg)
    l.place(relwidth=1, relheight=0.2, rely=0.25, relx=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.place(relwidth=0.5, relheight=0.2, rely=0.5, relx=0.25)

def encrypt_file():
    try:
        key = key_input.get()
        if len(key) > 0:
            encrypt_me = filedialog.askopenfilename(initialdir="/", title="Select a File to Encrypt")
            key = list(key)

            f = open(encrypt_me, 'rb')
            file = f.read()
            f.close()

            file = bytearray(file)
            for index, values in enumerate(file):
                file[index] = values ^ ord(key[index%len(key)])
    
            f = open(encrypt_me + ".enc", 'wb')
            f.write(file)
            f.close()
            pop_up("Encryption Done")
        else:
            pop_up("You need to enter a key first.")
    except:
        pop_up("Something Went Wrong.")

def decrypt_file():
    try:
        key = key_input.get()
        if len(key) > 0:
            decrypt_me = filedialog.askopenfilename(initialdir="/", title="Select a File to Decrypt")
        
            key = list(key)
        
            f = open(decrypt_me, 'rb')
            file = f.read()
            f.close()

            file = bytearray(file)
            for index, values in enumerate(file):
                file[index] = values ^ ord(key[index%len(key)])
    
            f = open(decrypt_me.replace(".enc", ""), 'wb')
            f.write(file)
            f.close()
            pop_up("Decryption Done")
        else:
            pop_up("You need to enter a key first.")
    except:
        pop_up("Something Went Wrong.")

def generate_checksum():
    try:
        path = filedialog.askopenfilename(initialdir="/", title="Select File to Create Checksum for")
        f = open(path, 'rb')
        file = f.read()
        file = bytearray(file)
        f.close()
        checksum = hashlib.sha256(file)
        f = open(path + ".chs", 'wb')
        f.write(checksum.hexdigest().encode('ascii'))
        f.close()
        pop_up("Checksum Created")
    except:
        pop_up("Something Went Wrong.")

def integrity_check():
    try:
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File to Check")
        chs_path = filedialog.askopenfilename(initialdir="/", title="Select a Checksum File")
        f = open(file_path, 'rb')
        file = f.read()
        file = bytearray(file)
        f.close()
        new_chs = hashlib.sha256(file)
        f = open(chs_path, 'rb')
        chs = f.readline()
        f.close()
        if chs.decode('ascii') == new_chs.hexdigest():
            pop_up('Integrity check succesful.')
        else:
            pop_up('Integrity check failed')
    except:
        pop_up('Something Went Wrong.')
            

def generate_key_code():
    try:
        key = key_input.get()
        if len(key) > 0:
            code = qrcode.make(key)
            code.save(downloads + '/key_code.png')
            pop_up("Code at " + downloads)
        else:
            pop_up("You need to enter a key first.")
    except:
        pop_up("Something Went Wrong.")
    
def decode_key_code():
    try:
        qr_code = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")))
        det = cv2.QRCodeDetector()
        code_str, _, _ = det.detectAndDecode(cv2.imread(qr_code))
        pop_up("Key is >> " + code_str)
    except:
        pop_up("Something went wrong.")

canvas = tk.Canvas(root, width=647, height=400, bg="#f0f0f0")
canvas.pack()

app_label = tk.Label(root, text="V-Enc", bg="#252a35", fg="#f0f0f0")
app_label.place(relheight=0.075, relwidth=1, relx=0, rely=0)

img = tk.PhotoImage(file="icon.png")
qr_label = tk.Label(root, image=img)
qr_label.place(relwidth=0.8, relheight=0.4 , rely=0.075, relx=0.1)

key_input = ttk.Entry(root, show="*",justify='center')
canvas.create_window(150,290,window=key_input, width=241, height=35)

btn = ttk.Button(root, text="Encrypt a File", command=encrypt_file)
btn.place(relwidth=0.4, relheight=0.1, relx=0.075, rely=0.55)

btn = ttk.Button(root, text="Decrypt a File", command=decrypt_file)
btn.place(relwidth=0.4, relheight=0.1, relx=0.525, rely=0.55)

btn = ttk.Button(root, text="Checksum\nGeneration", command=generate_checksum)
btn.place(relwidth=0.4, relheight=0.1, relx=0.075, rely=0.67)

btn = ttk.Button(root, text="  Integrity\nValidation", command=integrity_check)
btn.place(relwidth=0.4, relheight=0.1, relx=0.525, rely=0.67)

btn = ttk.Button(root, text=" Generate a QR\nCode of the Key", command=generate_key_code)
btn.place(relwidth=0.4, relheight=0.1, relx=0.075, rely=0.79)

btn = ttk.Button(root, text="Decode a\nKey Code", command=decode_key_code)
btn.place(relwidth=0.4, relheight=0.1, relx=0.525, rely=0.79)

by_label = tk.Label(root, text="by dekaottoman", bg="#252a35", fg="#f0f0f0")
by_label.place(relheight=0.075, relwidth=1, relx=0, rely=0.925)

root.mainloop()