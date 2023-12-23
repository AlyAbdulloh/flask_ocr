import numpy
from flask import Flask, request, jsonify
import cv2
import pytesseract
import re

app = Flask(__name__)

@app.route('/extract_info', methods=['POST'])
def extract_info():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    # Read the image and perform OCR
    image = cv2.imdecode(numpy.fromstring(file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    # image = cv2.imread("3A_2141720039_2.jpg")
    # cv2.imwrite("image.jpg", image)

    # do preprocessing for image so can easily read by tesseract
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    invert = cv2.bitwise_not(thresh)
    kernel = numpy.ones((1, 1), numpy.uint8)
    dilated = cv2.dilate(invert, kernel, iterations=2)

    # save image to local
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    text = pytesseract.image_to_string(dilated)

    # Extract information from the text
    # sections = text.split("\n\n")
    # teks = sections[0]
    teks = text
    kunci = "2141"
    pola_nim = re.compile(r'\b' + re.escape(kunci) + r'\d+\b')

    hasil_nim = pola_nim.search(teks)
    NIM="Tidak Ditemukan"

    if hasil_nim:
        nim_ditemukan = hasil_nim.group()
        NIM=nim_ditemukan

    # nama
    pola_nama = re.compile(r'\b([A-Z\s]+)\n')

    # Temukan semua kecocokan yang sesuai dengan pola
    hasil = pola_nama.search(teks)

    # Ambil hasil ekstraksi nama
    nama = "Tidak ditemukan"
    if hasil:
        nama = hasil.group(1).strip()
        # print(nama)
        
    # TTL

    pola_tanggal_tempat = re.compile(r'\b\n([A-Z][A-Z\s,]+)\s+(\d+\s+[A-Za-z]+\s+\d{4})')

    # Temukan semua kecocokan yang sesuai dengan pola
    hasil_ttl = pola_tanggal_tempat.search(teks)

    # Ambil hasil ekstraksi tanggal dan tempat
    ttl = "Tidak ditemukan"
    if hasil_ttl:
        tempat = hasil_ttl.group(1).strip()
        tanggal = hasil_ttl.group(2).strip()
        ttl = tempat+tanggal

    # Prodi
    # Definisikan pola regex untuk mengekstrak "DAV T. INFORMATIKA"
    pola_nama_program = re.compile(r'\b([A-Z]+\s[A-Z]+\.\s[A-Z\s]+)\b\n\n')

    # Temukan semua kecocokan yang sesuai dengan pola
    hasil_prodi = pola_nama_program.search(teks)

    nama_program = "Tidak ditemukan"
    # Ambil hasil ekstraksi "DAV T. INFORMATIKA"
    if hasil_prodi:
        nama_program = hasil_prodi.group(1).strip()

    result = {
        "NIM": NIM,
        'NAMA' : nama,
        'TTL' : ttl,
        'PRODI' : nama_program
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run('0.0.0.0' ,debug=True)