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
  apiKey: "GANTI_DENGAN_API_KEY_ANDA",
  authDomain: "GANTI_DENGAN_AUTH_DOMAIN_ANDA",
  projectId: "GANTI_DENGAN_PROJECT_ID_ANDA",
  storageBucket: "GANTI_DENGAN_STORAGE_BUCKET_ANDA",
  messagingSenderId: "GANTI_DENGAN_MESSAGING_SENDER_ID_ANDA",
  appId: "GANTI_DENGAN_APP_ID_ANDA"
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