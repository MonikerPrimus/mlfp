import pandas as pd
import numpy as np
import signal, sys
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from joblib import Memory
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up memory
memory = Memory(location='geocode_cache', verbose=0)

@memory.cache
def geocode_once(address):
    geolocator = Nominatim(user_agent="geo_app", timeout=10)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    for _ in range(2):
        loc = geocode(address)
        if loc:
            return loc.latitude, loc.longitude
    return None, None

# Save progress when code stops
df = pd.DataFrame()
def save_progress():
    df.to_csv("cleaned_data_partial.csv", index=False)
    print("\nProgress saved. Exiting code.")
    sys.exit(0)

signal.signal(signal.SIGINT, lambda sig, frame: save_progress())

def process_row(idx, addr):
    lat, lon = geocode_once(addr)
    if lat is not None:
        print(f"Row {idx}: -> lat: {lat:.6f}, lon: {lon:.6f}")
    else:
        print(f"Row {idx}: -> No location found")
    return idx, lat, lon

def main():
    global df
    df = pd.read_csv("cleaned_data.csv", low_memory=False)

    # Piece together the address
    df['full_address'] = (
        df['Recipient_Primary_Business_Street_Address_Line1'].fillna('') + ', ' +
        df['Recipient_City'].fillna('') + ', ' +
        df['Recipient_State'].fillna('') + ' ' +
        df['Recipient_Zip_Code'].astype(str).fillna('') + ', ' +
        df['Recipient_Country'].fillna('')
    )

    # Check duplicates for efficiency
    before = len(df)
    df = df.drop_duplicates(subset=['full_address'], keep='first').reset_index(drop=True)
    after = len(df)
    print(f"Removed {before - after} duplicate addresses; {after} unique rows remain.")

    # Set up columns
    df['latitude'] = np.nan
    df['longitude'] = np.nan

    # Multithreading for faster geocoding
    with ThreadPoolExecutor(max_workers=5) as exe:
        futures = {exe.submit(process_row, idx, addr): idx for idx, addr in enumerate(df['full_address'])}
        for future in as_completed(futures):
            idx, lat, lon = future.result()
            df.at[idx, 'latitude'] = lat
            df.at[idx, 'longitude'] = lon

    # Save completed data set
    df.to_csv("cleaned_data_with_latlon.csv", index=False)
    print(f"\n Completed geocoding {len(df)} unique addresses. Output saved.")

if __name__ == "__main__":
    main()