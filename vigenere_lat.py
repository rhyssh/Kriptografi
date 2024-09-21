import tkinter as tk
from tkinter import filedialog, messagebox

# Fungsi untuk enkripsi Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    key = key.upper()
    plaintext = plaintext.upper()
    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = (ord(char) - ord('A') + ord(key[key_index] ) - ord('A')) % 26
            ciphertext += chr(shift + ord('A'))
            key_index = (key_index + 1) % len(key)
        else:
            ciphertext += char
    return ciphertext

# Fungsi untuk dekripsi Vigenere Cipher
def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    ciphertext = ciphertext.upper()
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = (ord(char) - ord('A') - (ord(key[key_index]) - ord('A'))) % 26
            plaintext += chr(shift + ord('A'))
            key_index = (key_index + 1) % len(key)
        else:
            plaintext += char
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
    ciphertext = vigenere_encrypt(message, key)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, ciphertext)

# Fungsi untuk dekripsi pesan
def decrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get()
    if len(key) < 12:
        messagebox.showwarning("Error", "Panjang kunci minimal 12 karakter")
        return
    plaintext = vigenere_decrypt(message, key)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, plaintext)

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title("Vigenere Cipher")

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
