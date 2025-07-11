import pandas as pd
import qrcode

# Baca data siswa
df = pd.read_csv("datadpm.csv")

# Buat QR code dari ID
for index, row in df.iterrows():
    kode = str(row["ID"])
    nama = row["Nama"]
    img = qrcode.make(kode)
    filename = f"barcode/{kode} - {nama}.png"
    img.save(filename)
    print(f"✅ QR code dibuat: {filename}")
