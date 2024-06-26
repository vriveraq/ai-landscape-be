import os
import pandas as pd
import streamlit as st
from scripts.interactiveMap import get_location_interactive

# Define app using completed dataset
def main():
    st.title('Belgian AI Landscape')
    st.write('A list highlighting the companies focused on data science and artificial intelligence in Belgium.')

    filepath =  "data/AILandscape_geocoded.csv"
    database = pd.read_csv(filepath)
    
    region = st.multiselect('Regions: ', options = database['Region'].sort_values().unique(), default = database['Region'].sort_values().unique()) 
    city = st.multiselect('Cities: ', options = database['City'].sort_values().unique(), default = None)

    try:
        if city != []:
            df = database[database['City'].isin(city)]   
        else:
            df = database[database['Region'].isin(region)]
    

             
        figure = get_location_interactive(df)
        st.plotly_chart(figure)
        st.markdown(df[['Company Name', 'Link', 'Region', 'Address']].sort_values(by=['Company Name', 'Region']).to_html(render_links=True),unsafe_allow_html=True)
        csv = df.to_csv().encode('utf-8')
        st.download_button(
                "Press to Download",
                csv,
                "ai_be_file.csv",
                "text/csv",
                key='download-csv'
                )
    except KeyError:
        st.write('Please select a region or city!')

    link = '[GitHub source code](https://github.com/vriveraq/ai-landscape-be)'
    st.markdown(link, unsafe_allow_html=True)
if __name__ == '__main__':
    main()