import pandas as pd
import requests
import time

# --- PENGATURAN ---
OSRM_BASE_URL = "http://localhost:5000"
file_name = 'latlong_hub'
INPUT_CSV_FILE = f"input/{file_name}.csv"
OUTPUT_CSV_FILE = f"output/output_{file_name}_car.csv"

# --- PENGATURAN NAMA KOLOM ---
# Sesuaikan nama-nama ini dengan nama kolom di file CSV Anda
KOLOM_START_LON = 'BRANCH_LONGITUDE'
KOLOM_START_LAT = 'BRANCH_LATITUDE'
KOLOM_END_LON = 'SELECTED_LONGITUDE'
KOLOM_END_LAT = 'SELECTED_LATITUDE'
# -----------------------------


def get_osrm_route(start_lon, start_lat, end_lon, end_lat):
    """
    Meminta rute ke server OSRM dan mengembalikan jarak (km) dan durasi (menit).
    """
    url = f"{OSRM_BASE_URL}/route/v1/car/{start_lon},{start_lat};{end_lon},{end_lat}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 'Ok':
                route_summary = data['routes'][0]
                distance_km = route_summary['distance'] / 1000
                duration_min = route_summary['duration'] / 60
                return round(distance_km, 2), round(duration_min, 2)
    except requests.exceptions.RequestException as e:
        print(f"  -> Error koneksi ke OSRM: {e}")
    
    return None, None

def main():
    """
    Fungsi utama untuk membaca file, memproses rute, dan menyimpan hasil.
    """
    print(f"Membaca data dari {INPUT_CSV_FILE}...")
    try:
        df = pd.read_csv(INPUT_CSV_FILE)
    except FileNotFoundError:
        print(f"Error: File '{INPUT_CSV_FILE}' tidak ditemukan!")
        return

    df['jarak_km'] = None
    df['durasi_menit'] = None
    
    print("Memulai proses pencarian rute...")
    for index, row in df.iterrows():
        print(f"Memproses baris {index + 1}/{len(df)}...")
        
        # Ambil data lat-lon menggunakan nama kolom yang sudah diatur
        start_lat = row[KOLOM_START_LAT]
        start_lon = row[KOLOM_START_LON]
        end_lat = row[KOLOM_END_LAT]
        end_lon = row[KOLOM_END_LON]

        distance, duration = get_osrm_route(start_lon, start_lat, end_lon, end_lat)
        
        if distance is not None:
            df.loc[index, 'jarak_km'] = distance
            df.loc[index, 'durasi_menit'] = duration
        else:
            print(f"  -> Gagal mendapatkan rute untuk baris {index + 1}")
        
        time.sleep(0.1) 

    print(f"\nProses selesai. Menyimpan hasil ke {OUTPUT_CSV_FILE}...")
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    print("Selesai!")

if __name__ == "__main__":
    main()