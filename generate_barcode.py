import pandas as pd
import qrcode

# Baca data siswa
df = pd.read_excel("data.xlsx")

# Buat QR code dari ID
for index, row in df.iterrows():
    kode = str(row["ID"])
    nama = row["Nama"]
    img = qrcode.make(kode)
    filename = f"{kode} - {nama}.png"
    img.save(filename)
    print(f"✅ QR code dibuat: {filename}")
