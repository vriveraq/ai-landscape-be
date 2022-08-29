import os
import pandas as pd
import streamlit as st
from scripts.interactiveMap import get_location_interactive

# Define app using completed dataset
def main():
    st.title('Belgian AI Landscape')
    st.write('A list highlighting the companies focused on data science and artificial intelligence in Belgium.')

    filepath = os.path.join(os.path.dirname(__file__), "data/AILandscape_geocoded.csv")
    database = pd.read_csv(filepath)

    region = st.multiselect('Regions: ', options = database['Region'].unique().tolist().sort(), default = database['Region'].unique().tolist()) 
    city = st.multiselect('Cities: ', options = database['City'].unique().tolist().sort(), default = None)

    
    if city != []:
        df = database[database['City'].isin(city)]   
    else:
        df = database[database['Region'].isin(region)]
             
    figure = get_location_interactive(df)
    st.plotly_chart(figure)
    st.dataframe(df[['Company Name', 'Link', 'Region', 'Address']].sort_values(by=['Company Name']))
    
    csv = df.to_csv().encode('utf-8')
    st.download_button(
            "Press to Download",
            csv,
            "ai_be_file.csv",
            "text/csv",
            key='download-csv'
            )

  
if __name__ == '__main__':
    main()