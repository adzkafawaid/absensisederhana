from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime

import os

app = Flask(__name__)

# Load data siswa
DATA_SISWA = "datadpm.csv"
ABSEN_FILE = "absensi.csv"
df_siswa = pd.read_csv(DATA_SISWA)

# Buat file absensi kalau belum ada
if not os.path.exists(ABSEN_FILE):
    pd.DataFrame(columns=["ID", "Nama", "NIM","Jabatan", "Waktu"]).to_csv(ABSEN_FILE, index=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/absen", methods=["POST"])
def absen():
    id_scan = request.json.get("id")
    print(f"[DEBUG] ID hasil scan: '{id_scan}'")
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tanggal = datetime.now().strftime("%Y-%m-%d")
    # Pastikan ID di CSV dan hasil scan tidak ada spasi
    df_siswa["ID"] = df_siswa["ID"].astype(str).str.strip()
    id_scan = str(id_scan).strip()
    siswa_data = df_siswa[df_siswa["ID"] == id_scan]
    print(f"[DEBUG] Data siswa ditemukan: {not siswa_data.empty}")
    if not siswa_data.empty:
        nama = siswa_data.iloc[0]["Nama"] if "Nama" in siswa_data.columns else ""
        nim = siswa_data.iloc[0]["NIM"] if "NIM" in siswa_data.columns else ""
        jabatan = siswa_data.iloc[0]["Jabatan"] if "Jabatan" in siswa_data.columns else ""
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_absen = pd.read_csv(ABSEN_FILE)
        df_absen["ID"] = df_absen["ID"].astype(str).str.strip()
        # Cek apakah sudah absen di hari yang sama
        sudah_absen = not df_absen[(df_absen["ID"] == id_scan) & (df_absen["Waktu"].astype(str).str.startswith(tanggal))].empty
        if sudah_absen:
            return jsonify({"status": "sudah_absen", "nama": nama, "nim": nim, "jabatan": jabatan, "waktu": waktu})
        # Tulis ke file absensi
        df_absen = df_absen.append({
            "ID": id_scan,
            "Nama": nama,
            "NIM": nim,
            "Jabatan": jabatan,
            "Waktu": waktu
        }, ignore_index=True)
        df_absen.to_csv(ABSEN_FILE, index=False)
        return jsonify({"status": "success", "nama": nama, "nim": nim, "jabatan": jabatan, "waktu": waktu})
    else:
        print(f"[DEBUG] Data tidak ditemukan untuk ID: '{id_scan}'")
        return jsonify({"status": "notfound"}), 404

@app.route("/data_absen")
def data_absen():
    df_absen = pd.read_csv(ABSEN_FILE)
    data = df_absen.to_dict(orient="records")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
