import pandas as pd
import qrcode

# Baca data siswa
df = pd.read_excel("data.xlsx")

# Buat barcode dari ID
for index, row in df.iterrows():
    kode = str(row["ID"])
    nama = row["Nama"]

    # Buat QR code
    img = qrcode.make(kode)
    # Simpan dengan nama file "ID - Nama.png"
    filename = f"{kode} - {nama}.png"
    img.save(filename)
    print(f"✅ QR code dibuat: {filename}")
