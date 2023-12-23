import re

teks = "21417020017482414 \n ACHMAD ALY \n MOJOKERTO "

kunci = "2141"
pola_nim = re.compile(r'\b' + re.escape(kunci) + r'\d+\b')

hasil_nim = pola_nim.search(teks)

if hasil_nim:
    nim_ditemukan = hasil_nim.group()
    print(f"Angka yang ditemukan: {nim_ditemukan}")

    # Gunakan nim_ditemukan sebagai kunci untuk pencarian nama
    NIM = nim_ditemukan

    result = {
        "NIM": NIM
    }

    
    
