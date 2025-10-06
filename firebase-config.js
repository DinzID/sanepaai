// =================================================================================
// == PENTING: GANTI SEMUA NILAI PLACEHOLDER DI BAWAH INI! ==
// =================================================================================
//
// Anda harus mengganti nilai-nilai di bawah ini dengan konfigurasi Firebase project Anda.
// Anda bisa mendapatkan konfigurasi ini dari Firebase Console:
//
// 1. Buka Firebase Console: https://console.firebase.google.com/
// 2. Pilih project Anda.
// 3. Klik ikon gerigi (Settings) di sebelah "Project Overview", lalu pilih "Project settings".
// 4. Di tab "General", scroll ke bawah ke bagian "Your apps".
// 5. Pilih web app Anda.
// 6. Di bagian "Firebase SDK snippet", pilih "Config" dan salin objek konfigurasinya.
//
// =================================================================================

const firebaseConfig = {
    apiKey: "AIzaSyAAsSbq4bPAl2ahdqzV15adC1sWvFo3fX4",
    authDomain: "sanepaai.firebaseapp.com",
    projectId: "sanepaai",
    storageBucket: "sanepaai.firebasestorage.app",
    messagingSenderId: "16359172717",
    appId: "1:16359172717:web:de1a963a67bf7d60b7ed64"
  };


// Inisialisasi Firebase
try {
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();
  const db = firebase.firestore();
  console.log("Firebase berhasil diinisialisasi.");
} catch (e) {
  console.error("Kesalahan inisialisasi Firebase. Pastikan Anda sudah mengisi firebaseConfig dengan benar.", e);
  alert("Kesalahan konfigurasi Firebase. Silakan periksa file firebase-config.js dan isi dengan kredensial yang benar.");
}