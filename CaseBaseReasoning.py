import pandas as pd

# Membaca file input
file_path = 'd:\\Python\\restoran.xlsx'
data = pd.read_excel(file_path)

def fuzzification(pelayanan, harga):
    # Fuzzifikasi untuk kualitas pelayanan
    if pelayanan <= 30:
        pelayanan_buruk = 1
        pelayanan_baik = 0
    elif 30 < pelayanan < 70:
        pelayanan_buruk = (70 - pelayanan) / 40
        pelayanan_baik = (pelayanan - 30) / 40
    else:
        pelayanan_buruk = 0
        pelayanan_baik = 1

    # Fuzzifikasi untuk harga
    if harga <= 35000:
        harga_murah = 1
        harga_mahal = 0
    elif 35000 < harga < 45000:
        harga_murah = (45000 - harga) / 10000
        harga_mahal = (harga - 35000) / 10000
    else:
        harga_murah = 0
        harga_mahal = 1

    return pelayanan_buruk, pelayanan_baik, harga_murah, harga_mahal

def inferensi(pelayanan_buruk, pelayanan_baik, harga_murah, harga_mahal):
    # Aturan inferensi
    skor_buruk = max(min(pelayanan_buruk, harga_mahal), min(pelayanan_buruk, harga_murah))
    skor_biasa = max(min(pelayanan_baik, harga_mahal), min(pelayanan_buruk, harga_mahal))
    skor_baik = min(pelayanan_baik, harga_murah)
    return skor_buruk, skor_biasa, skor_baik

def defuzzification(skor_buruk, skor_biasa, skor_baik):
    # Defuzzifikasi menggunakan metode centroid sederhana
    return (skor_buruk * 25 + skor_biasa * 50 + skor_baik * 75) / (skor_buruk + skor_biasa + skor_baik)

def calculate_scores(data):
    results = []
    for _, row in data.iterrows():
        pelayanan_buruk, pelayanan_baik, harga_murah, harga_mahal = fuzzification(row['Pelayanan'], row['harga'])
        skor_buruk, skor_biasa, skor_baik = inferensi(pelayanan_buruk, pelayanan_baik, harga_murah, harga_mahal)
        skor_final = defuzzification(skor_buruk, skor_biasa, skor_baik)
        results.append((row['id Pelanggan'], row['Pelayanan'], row['harga'], skor_final))
    return results

def save_to_excel(results, output_path):
    # Menyimpan hasil ke file Excel
    df_results = pd.DataFrame(results, columns=['id Pelanggan', 'Pelayanan', 'Harga', 'Skor'])
    df_results = df_results.sort_values(by='Skor', ascending=False).head(5)
    df_results.to_excel(output_path, index=False)
    print(f"Hasil telah disimpan di {output_path}")

# Jalankan sistem fuzzy
results = calculate_scores(data)
output_file = 'd:\\Python\\peringkat.xlsx'
save_to_excel(results, output_file)
