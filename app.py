from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Load data siswa
DATA_SISWA = "data.xlsx"
ABSEN_FILE = "absensi.xlsx"
df_siswa = pd.read_excel(DATA_SISWA)

# Buat file absensi kalau belum ada
if not os.path.exists(ABSEN_FILE):
    pd.DataFrame(columns=["ID", "Nama", "Kelas", "Waktu"]).to_excel(ABSEN_FILE, index=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/absen", methods=["POST"])
def absen():
    id_scan = request.json.get("id")
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tanggal = datetime.now().strftime("%Y-%m-%d")
    siswa_data = df_siswa[df_siswa["ID"] == id_scan]
    if not siswa_data.empty:
        nama = siswa_data.iloc[0]["Nama"]
        kelas = siswa_data.iloc[0]["Kelas"]
        df_absen = pd.read_excel(ABSEN_FILE)
        # Cek apakah sudah absen di hari yang sama
        sudah_absen = not df_absen[(df_absen["ID"] == id_scan) & (df_absen["Waktu"].str.startswith(tanggal))].empty
        if sudah_absen:
            return jsonify({"status": "sudah_absen", "nama": nama, "kelas": kelas, "waktu": waktu})
        # Tulis ke file absensi
        df_absen = df_absen.append({
            "ID": id_scan,
            "Nama": nama,
            "Kelas": kelas,
            "Waktu": waktu
        }, ignore_index=True)
        df_absen.to_excel(ABSEN_FILE, index=False)
        return jsonify({"status": "success", "nama": nama, "kelas": kelas, "waktu": waktu})
    else:
        return jsonify({"status": "notfound"}), 404

@app.route("/data_absen")
def data_absen():
    df_absen = pd.read_excel(ABSEN_FILE)
    data = df_absen.to_dict(orient="records")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
