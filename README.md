# Anargya SD Card Data Reader

Repository ini digunakan untuk **membaca dan memvisualisasikan data yang tersimpan di dalam SD Card** hasil logging sistem Anargya.

---

## 📦 Prerequisites

Pastikan semua dependensi berikut sudah terinstall sebelum menggunakan repository ini.

### 1. MinGW (C/C++ Compiler)

Digunakan untuk meng-compile file `.c`.

- Download:  
  https://sourceforge.net/projects/mingw/
- Saat instalasi, pastikan package berikut dicentang:
  - `mingw32-base`
  - `mingw32-gcc-g++`
  - `msys-base`

> ⚠️ Pastikan MinGW sudah ditambahkan ke **PATH environment variable**.

---

### 2. Python

Digunakan untuk visualisasi data.

- Install Python melalui **Microsoft Store**
- Install library yang dibutuhkan:
```bash
pip install matplotlib
```

---

## 📖 Cara Membaca Data dari SD Card

1. Clone repository ini:
```bash
git clone <url-repository-ini>
```
Atau gunakan GitHub Desktop

2. Pindahkan file `.txt` hasil dump SD Card ke folder repository.

3. Salin **nama file `.txt`** yang ingin dibaca.

4. Buka file `decompilegeminitest2.c`, lalu cari baris berikut:
```c
const char *filename = "(namafile)";
```
Ganti `(namafile)` dengan nama file SD Card yang sudah dicopy.

5. Simpan file, lalu buka **Command Prompt / Terminal** dan masuk ke direktori repository.

6. Compile file C:
```bash
g++ decompilegeminitest2.c -o nama_executable
```

7. Jalankan executable dan arahkan output ke file:
```bash
nama_executable > nama_file_output.txt
```

8. Data hasil pembacaan SD Card akan tersimpan di file output tersebut.

---

## 📊 Visualisasi Data Raw

1. Buka file `visualizerawdata.py`
2. Ubah nilai `target_id` sesuai dengan jenis data yang ingin divisualisasikan  
   (lihat daftar ID di file **ID_DataSDCard**)
3. Jalankan:
```bash
python visualizerawdata.py
```

---

## 🌀 Visualisasi Data Gyroscope

1. Buka file `visualisasigyro.py`
2. Ganti nama file input dengan file output hasil pembacaan SD Card
3. Jalankan:
```bash
python visualisasigyro.py
```

---

## 📝 Catatan

- Pastikan format data SD Card sesuai dengan parser yang digunakan.
- Jika terjadi error saat kompilasi, periksa instalasi MinGW dan PATH.
- Visualisasi hanya dapat dilakukan setelah data berhasil didecode.

---

## 👨‍💻 Author

Anargya Team
