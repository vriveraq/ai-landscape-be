import numpy as np
# OpenStreetMap API
from geopy.geocoders import Nominatim

def get_geocoded_df(df):

    # After ensuring addresses have consistent formatting, we create new columns
    df[['Street','Location']] = df['Address'].str.split(",", n=1, expand=True)

    # Remove leading and trailing whitespaces
    df['Street'] = df['Street'].apply(lambda x: str(x).strip())
    df['Location'] = df['Location'].apply(lambda x: str(x).strip())

    df[['ZipCode','City']] = df['Location'].str.split(" ", n=1, expand=True)

    # We drop the missing values since these companies do not have an active website and their information is outdated. This is about 9 companies in total.
    print('Missing Addresses: ' +  str(df.isna().sum()))
    df.dropna(inplace=True)

    # We add the country to the address in preparation for our visualization
    df['Address'] = df['Address'].apply(lambda x: x + ', Belgium')

    # We use the address column to obtain the geocodes for each company
    geolocator = Nominatim(user_agent="http") 
    df['gcode'] = df['Address'].apply(geolocator.geocode)
    print('Missing Coordinates: ' + str(df['gcode'].isna().sum()))

    # Drop Missing Values
    df['gcode'].dropna(inplace = True)

    df['Latitude'] = [g.latitude if g is not None else np.nan for g in df.gcode ]
    df['Longitude'] = [g.longitude if g is not None else np.nan for g in df.gcode]
    df.to_csv('../data/AILandscape_geocoded.csv', index = False)

    return df