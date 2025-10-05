# Sanepa AI - Asisten AI Pribadi Anda

Sanepa AI adalah aplikasi web asisten AI yang canggih dan kaya fitur yang dirancang untuk memberikan pengalaman percakapan yang dinamis dan personal. Aplikasi ini terintegrasi dengan berbagai model AI, mendukung analisis gambar, dan dilengkapi dengan sistem otentikasi pengguna penuh menggunakan Firebase, termasuk peran admin khusus untuk manajemen terpusat.

## Fitur Utama

- **Dukungan Multi-Model**: Beralih dengan mudah antara berbagai model AI terkemuka seperti Gemini dan GPT-4o.
- **Analisis Gambar**: Unggah gambar dan ajukan pertanyaan tentangnya.
- **Mode Persona**: Sesuaikan kepribadian AI dengan mode seperti Teman, Asisten, Guru, atau bahkan Pacar Tsundere.
- **Kustomisasi Prompt**: Edit dan simpan prompt sistem kustom Anda sendiri untuk setiap mode.
- **Otentikasi Pengguna**: Sistem login dan registrasi yang aman menggunakan Firebase Authentication.
- **Sinkronisasi Cloud**: Pengaturan pengguna (jadwal, prompt kustom) disimpan dengan aman di Firestore dan disinkronkan di seluruh perangkat.
- **Panel Admin**: Panel khusus yang dilindungi untuk admin guna mengelola pengaturan global seperti prompt default dan jadwal.
- **Manajemen Jadwal**: Mode "Guru" yang cerdas dapat melacak dan mengingatkan jadwal pelajaran pengguna.
- **Tema Kustom**: Pilih antara tema Terang, Gelap, dan Ungu.
- **Desain Responsif**: Antarmuka yang bersih dan modern yang berfungsi baik di desktop maupun perangkat seluler.

## Penyiapan Firebase

Untuk menjalankan aplikasi ini dengan semua fitur otentikasinya, Anda perlu membuat proyek Firebase Anda sendiri. Ikuti langkah-langkah di bawah ini.

### Langkah 1: Buat Proyek Firebase

1.  Buka [Firebase Console](https://console.firebase.google.com/).
2.  Klik **"Add project"** dan ikuti petunjuk untuk membuat proyek baru. Beri nama apa saja yang Anda suka.

### Langkah 2: Tambahkan Aplikasi Web ke Proyek Anda

1.  Di dasbor proyek Anda, klik ikon Web (`</>`) untuk menambahkan aplikasi web baru.
2.  Beri nama panggilan pada aplikasi Anda (misalnya, "Sanepa AI Chat") dan klik **"Register app"**.
3.  Firebase akan menyediakan objek konfigurasi (`firebaseConfig`). **Salin objek ini.** Anda akan membutuhkannya segera.

### Langkah 3: Buat File `firebase-config.js`

1.  Di direktori root proyek Anda, buat file baru bernama `firebase-config.js`.
2.  Tempelkan objek `firebaseConfig` yang Anda salin ke dalam file ini dan inisialisasi Firebase. File Anda akan terlihat seperti ini:

    ```javascript
    // firebase-config.js

    // Ganti dengan konfigurasi proyek Firebase Anda
    const firebaseConfig = {
      apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      authDomain: "your-project-id.firebaseapp.com",
      projectId: "your-project-id",
      storageBucket: "your-project-id.appspot.com",
      messagingSenderId: "123456789012",
      appId: "1:123456789012:web:abcdef1234567890"
    };

    // Inisialisasi Firebase
    firebase.initializeApp(firebaseConfig);
    const auth = firebase.auth();
    const db = firebase.firestore();
    ```

### Langkah 4: Aktifkan Otentikasi

1.  Di Firebase Console, buka bagian **Authentication** (di bawah "Build").
2.  Buka tab **"Sign-in method"**.
3.  Aktifkan penyedia **"Email/Password"**.

### Langkah 5: Siapkan Firestore Database

1.  Buka bagian **Firestore Database** (di bawah "Build").
2.  Klik **"Create database"**.
3.  Mulai dalam **mode produksi** (production mode) dan klik "Next".
4.  Pilih lokasi Cloud Firestore yang paling dekat dengan pengguna Anda. Klik "Enable".

### Langkah 6: Atur Aturan Keamanan Firestore

Ini adalah langkah **KRUSIAL** untuk melindungi data pengguna.

1.  Di bagian Firestore Database, buka tab **"Rules"**.
2.  Ganti aturan default dengan yang berikut ini:

    ```
    rules_version = '2';
    service cloud.firestore {
      match /databases/{database}/documents {
        // Pengguna hanya dapat membaca/menulis data mereka sendiri
        match /users/{userId} {
          allow read, update, write: if request.auth != null && request.auth.uid == userId;
          allow create: if request.auth != null;
        }

        // Siapa pun dapat membaca pengaturan global (misalnya, prompt Guru default)
        match /settings/global {
          allow read: if true;
          // Hanya admin yang dapat menulis pengaturan global
          allow write: if request.auth != null && request.auth.uid == 'fVdAMsA5s3gA9p0xJ8rY2ZtQW1i1'; // Ganti dengan UID Admin Anda
        }
      }
    }
    ```

3.  **PENTING**: Ganti `'fVdAMsA5s3gA9p0xJ8rY2ZtQW1i1'` dengan **UID Admin Anda sendiri**. (Lihat langkah berikutnya).
4.  Klik **"Publish"**.

### Langkah 7: Dapatkan UID Admin Anda & Perbarui Kode

1.  **Daftarkan akun untuk admin**: Jalankan aplikasi, buka modal login/daftar, dan daftarkan pengguna yang akan menjadi admin.
2.  **Temukan UID**: Buka Firebase Console -> Authentication -> Users. Salin **UID** dari pengguna yang baru saja Anda daftarkan.
3.  **Perbarui Aturan Firestore**: Tempelkan UID yang disalin ke dalam aturan keamanan Firestore yang Anda atur pada Langkah 6.
4.  **Perbarui `index.html`**: Buka file `index.html`, cari baris `const ADMIN_UID = "fVdAMsA5s3gA9p0xJ8rY2ZtQW1i1";` dan ganti placeholder UID dengan UID Admin Anda sendiri.

## Cara Menjalankan

Setelah menyelesaikan penyiapan Firebase, cukup buka file `index.html` di browser web modern. Tidak diperlukan server lokal atau langkah build.