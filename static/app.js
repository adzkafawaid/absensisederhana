// Tambahkan log untuk debug
console.log("app.js loaded");
console.log("Html5Qrcode:", typeof Html5Qrcode);

let html5QrcodeScanner;
let isCameraOpen = false;
const readerDiv = document.getElementById('reader');
const openBtn = document.getElementById('openCam');
const closeBtn = document.getElementById('closeCam');
const cameraError = document.getElementById('camera-error');


openBtn.onclick = function() {
    cameraError.innerHTML = '';
    if (!isCameraOpen) {
        readerDiv.style.display = 'block';
        if (typeof Html5Qrcode === 'undefined') {
            cameraError.innerHTML = '❌ Library scanner tidak termuat. Pastikan koneksi internet dan refresh halaman.';
            return;
        }
        html5QrcodeScanner = new Html5Qrcode("reader");
        html5QrcodeScanner.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: 250 },
            onScanSuccess,
            onScanError
        ).then(() => {
            isCameraOpen = true;
            openBtn.style.display = 'none';
            closeBtn.style.display = 'inline-block';
        }).catch(err => {
            cameraError.innerHTML = '❌ Kamera gagal diakses: ' + err;
            readerDiv.style.display = 'none';
            isCameraOpen = false;
        });
    }
};
closeBtn.onclick = function() {
    if (isCameraOpen && html5QrcodeScanner) {
        html5QrcodeScanner.stop().then(() => {
            readerDiv.style.display = 'none';
            isCameraOpen = false;
            openBtn.style.display = 'inline-block';
            closeBtn.style.display = 'none';
        });
    }
};

function onScanSuccess(decodedText, decodedResult) {
    document.getElementById('result').innerHTML = 'Memproses...';
    fetch('/absen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: decodedText })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            document.getElementById('result').innerHTML = `✅ ${data.nama} (${data.kelas}) absen pada ${data.waktu}`;
            loadAbsen();
        } else if(data.status === 'sudah_absen') {
            document.getElementById('result').innerHTML = `⚠️ ${data.nama} (${data.kelas}) sudah absen hari ini!`;
        } else {
            document.getElementById('result').innerHTML = '❌ Data tidak ditemukan!';
        }
    })
    .catch(() => {
        document.getElementById('result').innerHTML = '❌ Gagal mengirim data!';
    });
    // Kamera tetap menyala, tidak close
}
function onScanError(err) {
    // Optional: tampilkan error scanning jika perlu
}
function loadAbsen() {
    fetch('/data_absen')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector('#absenTable tbody');
            tbody.innerHTML = '';
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${row.ID}</td><td>${row.Nama}</td><td>${row.Kelas}</td><td>${row.Waktu}</td>`;
                tbody.appendChild(tr);
            });
        });
}
loadAbsen();
setInterval(loadAbsen, 5000); // refresh setiap 5 detik
