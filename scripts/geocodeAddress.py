import numpy as np
# OpenStreetMap API
from geopy.geocoders import Nominatim

def create_geolocator(timeout = 10):
    geolocator = Nominatim(user_agent="http", timeout= timeout)
    return geolocator 

def create_address_column(df):
    # We create a column for the full address of the company
    cols = ["street","zip_code","city"]
    df.loc[:,'address'] = df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    return df

def geocode_address(address):
    geolocator = create_geolocator()
    try:
        geocoded_address = geolocator.geocode(address)
        return geocoded_address.latitude, geocoded_address.longitude
    except:
        return None, None