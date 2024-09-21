import tkinter as tk
from tkinter import filedialog, messagebox

def create_tabel(key):
    key = key.upper().replace("J", "I")
    tabel = []
    kotak = set()

    for char in key:
        if char not in kotak and char.isalpha():
            kotak.add(char)
            tabel.append(char)
    
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in kotak:
            kotak.add(char)
            tabel.append(char)

    return [tabel[i:i+5] for i in range(0, 25, 5)]

def posisi(char,tabel):
    for i, row in enumerate(tabel):
        if char in row:
            return (i, row.index(char))
    return None

def encrypt(plaintext, key):
    table = create_tabel(key)
    plaintext = plaintext.upper().replace('J', 'I').replace(' ', '')
    
    pairs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:  
                pairs.append(a + 'X')
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + 'X') 
            i += 1

    ciphertext = ''
    for pair in pairs:
        row1, column1 = posisi(pair[0], table)
        row2, column2 = posisi(pair[1], table)
        if row1 == row2:  # Dalam baris yang sama
            ciphertext += table[row1][(column1 + 1) % 5]
            ciphertext += table[row2][(column2 + 1) % 5]
        elif column1 == column2:  # Dalam kolom yang sama
            ciphertext += table[(row1 + 1) % 5][column1]
            ciphertext += table[(row2 + 1) % 5][column2]
        else:  # Dalam kotak
            ciphertext += table[row1][column2]
            ciphertext += table[row2][column1]

    return ciphertext

def decrypt(ciphertext, key):
    table = create_tabel(key)
    ciphertext = ciphertext.upper().replace(' ', '')
    
    pairs = []
    i = 0
    while i < len(ciphertext):
        pairs.append(ciphertext[i:i + 2])
        i += 2

    plaintext = ''
    for pair in pairs:
        row1, column1 = posisi(pair[0], table)
        row2, column2 = posisi(pair[1], table)
        if row1 == row2:  # Dalam baris yang sama
            plaintext += table[row1][(column1 - 1) % 5]
            plaintext += table[row2][(column2 - 1) % 5]
        elif column1 == column2:  # Dalam kolom yang sama
            plaintext += table[(row1 - 1) % 5][column1]
            plaintext += table[(row2 - 1) % 5][column2]
        else:  # Dalam kotak
            plaintext += table[row1][column2]
            plaintext += table[row2][column1]

    return plaintext


# Fungsi untuk upload file
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        text_input.delete('1.0', tk.END)
        text_input.insert(tk.END, data)

# Fungsi untuk enkripsi pesan
def encrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get()
    if len(key) < 12:
        messagebox.showwarning("Error", "Panjang kunci minimal 12 karakter")
        return
    ciphertext = encrypt(message, key)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, ciphertext)

# Fungsi untuk dekripsi pesan
def decrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get()
    if len(key) < 12:
        messagebox.showwarning("Error", "Panjang kunci minimal 12 karakter")
        return
    plaintext = decrypt(message, key)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, plaintext)

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title("Playfair Cipher")

# Membuat layout untuk input pesan
text_input_label = tk.Label(root, text="Input Pesan:")
text_input_label.pack()
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# Membuat tombol untuk upload file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack()

# Input untuk kunci enkripsi
key_label = tk.Label(root, text="Masukkan Kunci (minimal 12 karakter):")
key_label.pack()
key_input = tk.Entry(root)
key_input.pack()

# Tombol untuk enkripsi dan dekripsi
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_message)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)
decrypt_button.pack()

# Area untuk menampilkan hasil
result_label = tk.Label(root, text="Hasil:")
result_label.pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()