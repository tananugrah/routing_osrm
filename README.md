
# Dokumentasi Proyek Server Rute OSRM Lokal

Dokumen ini menjelaskan cara melakukan setup, instalasi, dan penggunaan server perutean OSRM lokal menggunakan Docker. Proyek ini dikonfigurasi untuk menghitung rute mobil (car) dan dilengkapi dengan script Python untuk memproses banyak rute dari file CSV.

-----

## 1\. Ringkasan Proyek

Proyek ini bertujuan untuk:

1.  Menjalankan instance OSRM (Open Source Routing Machine) secara lokal di dalam container Docker.
2.  Melakukan pra-pemrosesan data peta dari OpenStreetMap (format .osm.pbf) untuk wilayah Indonesia.
3.  Menyediakan API perutean yang dapat diakses di `http://localhost:5000`.
4.  Menjalankan script Python untuk membaca koordinat dari file CSV, meminta data jarak dan durasi ke server OSRM, dan menyimpan hasilnya kembali ke file CSV baru.

-----

## 2\. Prasyarat

Sebelum memulai, pastikan perangkat Anda sudah terinstal:

  * **Docker Desktop**: Dengan backend WSL 2 jika Anda menggunakan Windows.
  * **Python 3.x**: Untuk menjalankan script pemroses data.
  * **Library Python**: Install library yang dibutuhkan dengan perintah berikut di terminal:
    ```bash
    pip install pandas openpyxl requests
    ```

-----

## 3\. Struktur File Proyek

Atur folder proyek Anda dengan struktur seperti berikut:

```
/proyek-osrm/
|-- /input
|-- /output
|-- /osrm-data/
|   |-- indonesia-latest.osm.pbf  <-- (File Peta, diunduh manual)
|-- docker-compose.yml
|-- search_rute.py
```

-----

## 4\. Langkah-langkah Instalasi & Setup

### 4.1. Unduh Data Peta OSM

Unduh data peta OpenStreetMap untuk wilayah yang Anda inginkan (contoh: Indonesia) dalam format .osm.pbf.

  * **Sumber**: Geofabrik Download Server
  * **Tindakan**: Simpan file `indonesia-latest.osm.pbf` di dalam folder `osrm-data`.

### 4.2. Buat File `docker-compose.yml`

Buat file `docker-compose.yml` di folder utama proyek dan salin kode berikut. File ini mendefinisikan dua layanan: `osrm_processor` (untuk memproses data sekali jalan) dan `osrm_router` (untuk menjalankan server API).


### 4.3. Jalankan Server OSRM

1.  Buka terminal di folder utama proyek Anda.
2.  Jalankan perintah berikut untuk memulai proses:
    ```bash
    docker compose -f docker-compose.osrm.yml up --build -d
    ```
3.  Pada saat pertama kali dijalankan, `osrm_processor` akan memproses file .pbf. Proses ini sangat lama dan membutuhkan banyak RAM (disarankan 8GB+). Anda bisa memantau progresnya dengan:
    ```bash
    docker logs -f osrm_processor
    ```
4.  Setelah proses selesai, `osrm_processor` akan berhenti dan `osrm_router` akan berjalan secara otomatis, siap menerima permintaan.
5.  Pada saat dijalankan kembali, `osrm_processor` akan melihat data sudah ada, langsung berhenti, dan `osrm_router` akan segera dimulai.

-----

## 5\. Cara Penggunaan Script Python

### 5.1. Siapkan File Input CSV

Buat file bernama `/input/data_lokasi.csv` dengan format header dan data sebagai berikut:

```csv
BRANCH_LON,BRANCH_LAT,SELECTED_LON,SELECTED_LAT
106.8993,-6.1642,106.9115,-6.16702
120.31,-4.55015,120.3823,-4.5337
104.0678,-4.55727,104.1022,-4.57383
```

### 5.2. Siapkan Script Python

Buat file `search_rute.py` dan salin kode di bawah. Anda bisa mengubah nama file input/output dan nama kolom di bagian PENGATURAN.

### 5.3. Jalankan Script

Pastikan server OSRM Anda sudah berjalan, lalu jalankan script dari terminal:

```bash
python search_rute.py
```

Hasilnya akan tersimpan pada folder output dengan tambahan kolom `jarak_km` dan `durasi_menit`.

-----

## 6\. Troubleshooting Umum

  * **Proses berhenti mendadak**: Kemungkinan besar karena kehabisan RAM. Naikkan alokasi memori untuk Docker Desktop / WSL.
  * **`Required files are missing`**: Terjadi karena ketidakcocokan algoritma. Pastikan `osrm_router` dijalankan dengan command: `osrm-routed --algorithm CH`.
  * **Hasil jarak/durasi tidak akurat**: Masalahnya kemungkinan besar ada pada kualitas data OpenStreetMap atau ketidakcocokan asumsi kecepatan pada `profil.lua` yang digunakan.
