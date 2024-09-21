import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np


def encrypt(plaintext, matrix):
    plaintext = plaintext.upper()
    while len(plaintext) % len(matrix) != 0:
        plaintext += 'X'
    chipertext = ''
    for i in range(0,len(plaintext),len(matrix)):
        blok = plaintext[i:i+len(matrix)]
        vektor = [ord(char) - ord('A') for char in blok]
        encryptedVektor = kali_matrix(matrix,vektor)
        encryptedVektor = [val % 26 for val in encryptedVektor]
        ciphertextBlok = ''.join([chr(num + ord('A')) for num in encryptedVektor])
        chipertext += ciphertextBlok

    return chipertext

def decrypt(ciphertext, matrix):
    ciphertext = ciphertext.upper().replace(" ", "")
    determinan = int(np.round(np.linalg.det(matrix)))  # Determinan matriks
    determinan = determinan % 26 
    inv_determinan = mod_inverse(determinan, 26)  # Mencari invers modular dari determinan

    if inv_determinan is None:
        messagebox.showerror("Error", "tidak bisa mendekripsi, kunci tidak memiliki invers modular.")
        return ""

    adjugasi_matrix = matrix_adjugate(matrix)
    inverse_key_matrix = [[(inv_determinan * adjugasi_matrix[i][j]) % 26 for j in range(len(adjugasi_matrix))] for i in range(len(adjugasi_matrix))]

    plaintext = ""
    for i in range(0, len(ciphertext), len(inverse_key_matrix)):
        blok = ciphertext[i:i + len(inverse_key_matrix)]
        vektor = [ord(char) - ord('A') for char in blok]
        decrypted_vektor = kali_matrix(inverse_key_matrix, vektor)
        decrypted_vektor = [val % 26 for val in decrypted_vektor]  # Mod 26
        plaintext_blok = ''.join([chr(num + ord('A')) for num in decrypted_vektor])
        plaintext += plaintext_blok
    return plaintext

def kali_matrix(matrix,vektor):
    result = []
    for row in matrix:
        result.append(sum(row[i] * vektor[i] for i in range(len(vektor))))
    return result

def detemin_matrix(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif len(matrix) > 2:
        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[0][2]
        d = matrix[1][0]
        e = matrix[1][1]
        f = matrix[1][2]
        g = matrix[2][0]
        h = matrix[2][1]
        i = matrix[2][2]
        # Menggunakan rumus determinan 3x3
        determinant = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
        return determinant
    else:
        raise ValueError("Hanya matriks 2x2 yang didukung untuk sekarang.")

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None  # Tidak ada invers modular

def matrix_adjugate(matrix):
    if len(matrix) == 2:
        return [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]
    elif len(matrix) > 2:
        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[0][2]
        d = matrix[1][0]
        e = matrix[1][1]
        f = matrix[1][2]
        g = matrix[2][0]
        h = matrix[2][1]
        i = matrix[2][2]

        # kofaktor tiap elemen
        cofactor_matrix = [
            [
                (e * i - f * h), -(d * i - f * g), (d * h - e * g)
            ],
            [
                -(b * i - c * h), (a * i - c * g), -(a * h - b * g)
            ],
            [
                (b * f - c * e), -(a * f - c * d), (a * e - b * d)
            ]
        ]

        # transpose
        adjugate_matrix = [
            [cofactor_matrix[0][0], cofactor_matrix[1][0], cofactor_matrix[2][0]],
            [cofactor_matrix[0][1], cofactor_matrix[1][1], cofactor_matrix[2][1]],
            [cofactor_matrix[0][2], cofactor_matrix[1][2], cofactor_matrix[2][2]]
        ]
        return adjugate_matrix
    else:
        raise ValueError("Hanya matriks 2x2 yang didukung untuk sekarang.")
    
def string_matriks(key, size):
    key = key.upper().replace(" ", "")
    if len(key) != size * size:
        messagebox.showwarning("Error", f"Kunci harus terdiri dari {size * size} huruf.")
        return None
    matrix = []
    for i in range(size):
        row = [ord(char) - ord('A') for char in key[i*size:(i+1)*size]]
        matrix.append(row)
    return matrix

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        text_input.delete('1.0', tk.END)
        text_input.insert(tk.END, data)

def encrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    matrix_size = int(matrix_size_input.get())

    if len(key) != matrix_size * matrix_size:
        messagebox.showwarning("Error", f"Panjang kunci harus {matrix_size * matrix_size} karakter.")
        return

    key_matrix = string_matriks(key, matrix_size)
    if key_matrix is None:
        return

    ciphertext = encrypt(message, key_matrix)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, ciphertext)

def decrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    matrix_size = int(matrix_size_input.get())

    if len(key) != matrix_size * matrix_size:
        messagebox.showwarning("Error", f"Panjang kunci harus {matrix_size * matrix_size} karakter.")
        return

    key_matrix = string_matriks(key, matrix_size)
    if key_matrix is None:
        return

    plaintext = decrypt(message, key_matrix)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, plaintext)



root = tk.Tk()
root.title("Hill Cipher")

# Membuat layout untuk input pesan
text_input_label = tk.Label(root, text="Input Pesan:")
text_input_label.pack()
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# Membuat tombol untuk upload file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack()

# Input untuk kunci enkripsi
key_label = tk.Label(root, text="Masukkan Kunci (harus sesuai dengan ukuran matriks):")
key_label.pack()
key_input = tk.Entry(root)
key_input.pack()

# Input untuk ukuran matriks
matrix_size_label = tk.Label(root, text="Ukuran Matriks (contoh: 2 untuk 2x2, 3 untuk 3x3):")
matrix_size_label.pack()
matrix_size_input = tk.Entry(root)
matrix_size_input.pack()

# Tombol untuk enkripsi dan dekripsi
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_message)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)

encrypt_button.pack()
decrypt_button.pack( )

# Area untuk menampilkan hasil
result_label = tk.Label(root, text="Hasil:")
result_label.pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()
