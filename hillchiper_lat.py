import tkinter as tk
from tkinter import filedialog, messagebox

# Fungsi untuk enkripsi Hill Cipher (tanpa numpy)
def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.upper().replace(" ", "")
    # Pastikan panjang plaintext bisa dibagi dengan ukuran matriks
    while len(plaintext) % len(key_matrix) != 0:
        plaintext += 'X'  # Menambahkan 'X' jika diperlukan

    ciphertext = ""
    for i in range(0, len(plaintext), len(key_matrix)):
        block = plaintext[i:i + len(key_matrix)]
        vector = [ord(char) - ord('A') for char in block]
        encrypted_vector = matrix_multiply(key_matrix, vector)  # Operasi perkalian matriks
        encrypted_vector = [val % 26 for val in encrypted_vector]  # Mod 26
        ciphertext_block = ''.join([chr(num + ord('A')) for num in encrypted_vector])
        ciphertext += ciphertext_block

    return ciphertext

# Fungsi untuk dekripsi Hill Cipher (tanpa numpy)
def hill_decrypt(ciphertext, key_matrix):
    ciphertext = ciphertext.upper().replace(" ", "")
    determinant = matrix_determinant(key_matrix)  # Determinan matriks
    determinant_inv = mod_inverse(determinant, 26)

    if determinant_inv is None:
        messagebox.showerror("Error", "Kunci tidak memiliki invers modular, tidak bisa mendekripsi.")
        return ""

    adjugate_matrix = matrix_adjugate(key_matrix)  # Matriks adjugate
    inverse_key_matrix = [[(determinant_inv * adjugate_matrix[i][j]) % 26 for j in range(len(adjugate_matrix))] for i in range(len(adjugate_matrix))]

    plaintext = ""
    for i in range(0, len(ciphertext), len(inverse_key_matrix)):
        block = ciphertext[i:i + len(inverse_key_matrix)]
        vector = [ord(char) - ord('A') for char in block]
        decrypted_vector = matrix_multiply(inverse_key_matrix, vector)
        decrypted_vector = [val % 26 for val in decrypted_vector]  # Mod 26
        plaintext_block = ''.join([chr(num + ord('A')) for num in decrypted_vector])
        plaintext += plaintext_block

    return plaintext

# Fungsi untuk mengalikan dua matriks
def matrix_multiply(matrix, vector):
    result = []
    for row in matrix:
        result.append(sum(row[i] * vector[i] for i in range(len(vector))))
    return result

# Fungsi untuk menghitung determinan dari matriks 2x2
def matrix_determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        raise ValueError("Hanya matriks 2x2 yang didukung untuk sekarang.")

# Fungsi untuk menghitung invers modular
def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# Fungsi untuk menghitung adjugate matriks 2x2
def matrix_adjugate(matrix):
    if len(matrix) == 2:
        return [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]
    else:
        raise ValueError("Hanya matriks 2x2 yang didukung untuk sekarang.")

# Fungsi untuk mengonversi string kunci menjadi matriks
def string_to_matrix(key, size):
    key = key.upper().replace(" ", "")
    if len(key) != size * size:
        messagebox.showwarning("Error", f"Kunci harus terdiri dari {size * size} huruf.")
        return None

    matrix = []
    for i in range(size):
        row = [ord(char) - ord('A') for char in key[i*size:(i+1)*size]]
        matrix.append(row)

    return matrix

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
    key = key_input.get().strip()
    matrix_size = int(matrix_size_input.get())

    if len(key) != matrix_size * matrix_size:
        messagebox.showwarning("Error", f"Panjang kunci harus {matrix_size * matrix_size} karakter.")
        return

    key_matrix = string_to_matrix(key, matrix_size)
    if key_matrix is None:
        return

    ciphertext = hill_encrypt(message, key_matrix)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, ciphertext)

# Fungsi untuk dekripsi pesan
def decrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    matrix_size = int(matrix_size_input.get())

    if len(key) != matrix_size * matrix_size:
        messagebox.showwarning("Error", f"Panjang kunci harus {matrix_size * matrix_size} karakter.")
        return

    key_matrix = string_to_matrix(key, matrix_size)
    if key_matrix is None:
        return

    plaintext = hill_decrypt(message, key_matrix)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, plaintext)

# Membuat GUI menggunakan Tkinter
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
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)
decrypt_button.pack()

# Area untuk menampilkan hasil
result_label = tk.Label(root, text="Hasil:")
result_label.pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()
