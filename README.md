# 💧 AQUAPAVE

AQUAPAVE adalah platform berbasis Streamlit untuk optimasi desain perkerasan berpori ZEOPAVE-AQUA. Website ini dikembangkan untuk membantu analisis campuran beton berpori, permeabilitas, kuat tekan, retensi air, efisiensi biaya, serta dampak lingkungan secara interaktif.

Platform ini mendukung penelitian dan simulasi mitigasi banjir melalui sistem perkerasan berpori dengan pemanfaatan material alternatif seperti lumpur IPAL, zeolit, dan hebel AAC.

---

## ✨ Fitur Utama

### 🧮 Kalkulator Mix Design
- Menghitung komposisi campuran beton berpori
- Simulasi penggunaan:
  - Semen OPC
  - Lumpur IPAL
  - Batu sirtu
  - Hebel AAC
  - Zeolit
- Estimasi:
  - Porositas
  - Permeabilitas
  - Kuat tekan

### 💧 Analisis Permeabilitas
- Perhitungan metode Constant Head
- Mengacu pada SNI 2435:2008
- Mendukung multi-pengujian dan visualisasi hasil

### 🏗️ Analisis Kuat Tekan
- Perhitungan kuat tekan silinder beton
- Konversi ekuivalen umur 28 hari
- Mengacu pada SNI 1974:2011

### 🌊 Simulator Retensi Air
- Simulasi limpasan air hujan
- Estimasi kapasitas retensi sistem ZEOPAVE-AQUA
- Visualisasi aliran air menggunakan diagram Sankey

### 🌿 Emisi CO₂ & Efisiensi Material
- Estimasi emisi karbon
- Perbandingan beton konvensional vs ZEOPAVE-AQUA
- Analisis pengurangan penggunaan semen OPC

### 📊 Dasbor Perbandingan
- Perbandingan kinerja ZEOPAVE-AQUA dengan perkerasan konvensional
- Radar chart dan tabel analisis teknis

### 💰 Estimasi Biaya
- Perhitungan biaya material dan proyek
- Analisis sensitivitas biaya
- Perbandingan dengan perkerasan konvensional

---

## 🛠️ Teknologi yang Digunakan

- Python
- Streamlit
- NumPy
- Pandas
- Plotly

---

## 📦 Instalasi

### 1. Clone repository

```bash
git clone https://github.com/username/aquapave.git
cd aquapave