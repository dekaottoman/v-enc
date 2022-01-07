import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import hashlib
import os
import qrcode
import cv2
from vernam import encryption, decryption
from integrity import create_checksum, check_integrity

root = tk.Tk()
root.maxsize(647,400)
root.minsize(647,400)
root.title('V Enc')

if os.name == "nt":
    downloads = f"{os.getenv('USERPROFILE')}\\Downloads"
else:
    downloads = f"{os.getenv('HOME')}/Downloads"

def pop_up(msg:str):
    win = tk.Toplevel()
    win.wm_title("For you!")
    win.maxsize(243,150)
    win.minsize(243,150)

    l = tk.Label(win, text=msg)
    l.place(relwidth=1, relheight=0.2, rely=0.25, relx=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.place(relwidth=0.5, relheight=0.2, rely=0.5, relx=0.25)

def encrypt_file():
    key = key_input.get()
    if len(key) > 0:
        encrypt_me = filedialog.askopenfilename(initialdir="/", title="Select a File to Encrypt")
        encryption(encrypt_me, key)
        pop_up("Encryption Done")
    else:
        pop_up("You need to enter a key first.")

def decrypt_file():
    key = key_input.get()
    if len(key) > 0:
        decrypt_me = filedialog.askopenfilename(initialdir="/", title="Select a File to Decrypt")
        decryption(decrypt_me, key)
        pop_up("Decryption Done")
    else:
        pop_up("You need to enter a key first.")

def generate_checksum():
    path = filedialog.askopenfilename(initialdir="/", title="Select File to Create Checksum for")
    create_checksum(path)
    pop_up("Checksum Created")

def integrity_check():
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
        return True
    else:
        pop_up('Integrity check failed')
        return False

def generate_key_code():
    key = key_input.get()
    if len(key) > 0:
        code = qrcode.make(key)
        code.save(downloads + '/key_code.png')
        pop_up("Code at " + downloads)
    else:
        pop_up("You need to enter a key first.")
    
def decode_key_code():
    qr_code = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")))
    det = cv2.QRCodeDetector()
    code_str, _, _ = det.detectAndDecode(cv2.imread(qr_code))
    pop_up("Key is >> " + code_str)

canvas = tk.Canvas(root, width=647, height=400, bg="#f0f0f0")
canvas.pack()

app_label = tk.Label(root, text="Vernam Encryption App", bg="#227093", fg="#ffffff")
app_label.place(relheight=0.075, relwidth=1, relx=0, rely=0)

img = tk.PhotoImage(file="dekaottoman.png")
qr_label = tk.Label(root, image=img)
qr_label.place(width=275, height=275 , rely=0.15, relx=0.525)

key_input = ttk.Entry(root)
canvas.create_window(162,80,window=key_input, width=241, height=35)

btn = ttk.Button(root, text="Encrypt a File", command=encrypt_file)
btn.place(relwidth=0.375, relheight=0.077, relx=0.0625, rely=0.270)

btn = ttk.Button(root, text="Decrypt a File", command=decrypt_file)
btn.place(relwidth=0.375, relheight=0.077, relx=0.0625, rely=0.367)

btn = ttk.Button(root, text="Generate Checksum for a File", command=generate_checksum)
btn.place(relwidth=0.375, relheight=0.077, relx=0.0625, rely=0.464)

btn = ttk.Button(root, text="Validate File Integrity", command=integrity_check)
btn.place(relwidth=0.375, relheight=0.077, relx=0.0625, rely=0.561)

btn = ttk.Button(root, text="Generate a QR Code of the Key", command=generate_key_code)
btn.place(relwidth=0.375, relheight=0.077, relx=0.0625, rely=0.658)

btn = ttk.Button(root, text="Decode a Key Code", command=decode_key_code)
btn.place(relwidth=0.375, relheight=0.077, relx=0.0625, rely=0.755)

by_label = tk.Label(root, text="by dekaottoman", bg="#227093", fg="#ffffff")
by_label.place(relheight=0.075, relwidth=1, relx=0, rely=0.925)

root.mainloop()
