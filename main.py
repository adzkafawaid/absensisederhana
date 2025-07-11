import cv2
from pyzbar.pyzbar import decode
import pandas as pd
from datetime import datetime
import os

# Load data siswa (ID, Nama, Kelas)
df_siswa = pd.read_excel("data.xlsx")

# Buat file absensi kalau belum ada
absen_file = "absensi.xlsx"
if not os.path.exists(absen_file):
    pd.DataFrame(columns=["ID", "Nama", "Kelas", "Waktu"]).to_excel(absen_file, index=False)

# Mulai kamera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Kamera tidak dapat dibuka. Pastikan kamera terhubung dan tidak digunakan aplikasi lain.")
    exit(1)

while True:
    success, frame = cap.read()
    if not success or frame is None:
        print("[ERROR] Gagal membaca frame dari kamera.")
        break
    for barcode in decode(frame):
        id_scan = barcode.data.decode('utf-8')
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cek ID di data siswa
        siswa_data = df_siswa[df_siswa["ID"] == id_scan]

        if not siswa_data.empty:
            nama = siswa_data.iloc[0]["Nama"]
            kelas = siswa_data.iloc[0]["Kelas"]
            print(f"[INFO] {nama} dari {kelas} tercatat pada {waktu}")

            # Tulis ke file absensi
            df_absen = pd.read_excel(absen_file)
            df_absen = df_absen.append({
                "ID": id_scan,
                "Nama": nama,
                "Kelas": kelas,
                "Waktu": waktu
            }, ignore_index=True)
            df_absen.to_excel(absen_file, index=False)

            # Tunggu sebentar biar tidak double scan
            cv2.waitKey(2000)

    cv2.imshow("Scan Barcode", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
