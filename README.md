# 🤖 Aplikasi Deteksi Objek Real-Time dengan YOLOv8 & Streamlit

Aplikasi web interaktif ini dibangun menggunakan Python, Streamlit, dan model YOLOv8 untuk melakukan deteksi serta pelacakan objek secara *real-time* melalui kamera webcam atau dari file video yang diunggah.

---

## 🚀 Demo Langsung

Anda bisa langsung mencoba aplikasi ini tanpa perlu instalasi melalui link berikut:
Direkomendasikan Coba pada saat Jam 00:00 - 08:00 Pagi karena Server lebih cepat untuk akses kamera.

**🌐 Kunjungi Website: [[https://simple-object-detection.streamlit.app/](https://simple-object-detection.streamlit.app/)]** 

---

## 📸 Tampilan Aplikasi

Berikut adalah tampilan antarmuka aplikasi saat sedang berjalan.

![[Tampilan Aplikasi](https://github.com/TinoIf/object-detection/blob/main/tampilan-aplikasi-2.jpg)]
Tampilan Bisa Dilihat pada File repository ini untuk Hasilnya


---

## ✨ Fitur Utama

* **Deteksi Objek Real-Time**: Menggunakan kamera webcam untuk mendeteksi objek secara langsung.
* **Deteksi dari File Video**: Kemampuan untuk mengunggah file video (MP4, MOV, AVI) dan memprosesnya.
* **Pelacakan Objek (Tracking)**: Setiap objek yang terdeteksi diberikan ID unik yang konsisten antar frame.
* **Model YOLOv8**: Ditenagai oleh model YOLOv8n yang cepat dan ringan.
* **Pengaturan Interaktif**: Terdapat *slider* untuk menyesuaikan tingkat kepercayaan (*confidence threshold*) deteksi.

---

## 🛠️ Teknologi yang Digunakan

* **Python 3.9+**
* **Streamlit** - Untuk membangun antarmuka web interaktif.
* **Ultralytics (YOLOv8)** - Untuk model deteksi objek.
* **OpenCV** - Untuk pemrosesan gambar dan video.
* **Streamlit-WebRTC** - Untuk komponen streaming kamera *real-time*.

---

## ⚙️ Menjalankan Proyek Secara Lokal

Jika Anda ingin menjalankan aplikasi ini di komputer Anda sendiri, ikuti langkah-langkah berikut.

### 1. Prasyarat

Pastikan Anda sudah menginstal:
* [Python](https://www.python.org/downloads/) (disarankan versi 3.9 - 3.12)
* [Git](https://git-scm.com/downloads/)

### 2. Instalasi

**a. Clone Repository Ini**
Buka terminal atau Git Bash, lalu jalankan perintah berikut:

  git clone [[https://github.com/]([[https://github.com/](https://github.com/TinoIf/object-detection.git)])[TinoIf]/[object-detection].git]
  cd object-detection
  
  b. Buat dan Aktifkan Virtual Environment
  Sangat disarankan untuk menggunakan virtual environment agar tidak mengganggu instalasi Python utama Anda.
  
  Bash
  
  # Buat environment baru bernama "venv"
  ```
  python -m venv venv
  ```
  # Aktifkan environment
  # Di Windows:
  ```
  venv\Scripts\activate
  ```
  # Di macOS/Linux:
  ```
  source venv/bin/activate
  ```
  c. Instal Semua Dependensi
  Semua library yang dibutuhkan sudah terdaftar di requirements.txt. Instal semuanya dengan satu perintah:
  
  Bash
  ```
  pip install -r requirements.txt
  ```
  3. Menjalankan Aplikasi
  Setelah semua dependensi terinstal, jalankan aplikasi Streamlit dengan perintah:
  
  Bash
  ```
  streamlit run app.py
  ```
  Aplikasi akan otomatis terbuka di browser Anda pada alamat seperti http://localhost:8501.
