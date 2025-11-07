import os
import pandas as pd
import streamlit as st
from scripts.interactiveMap import get_location_interactive

# Define app using completed dataset
def main():
    st.title('Belgian AI Landscape')
    st.write('A list highlighting the companies focused on data science and artificial intelligence in Belgium.')

    filepath =  "data/geocoded_dataset.csv"
    database = pd.read_csv(filepath)
    
    region = st.multiselect('Regions: ', options = database['region'].sort_values().unique(), default = database['region'].sort_values().unique()) 
    city = st.multiselect('Cities: ', options = database['city'].sort_values().unique(), default = None)

    try:
        
        if city != []:
            df = database[database['city'].isin(city)]   
        else:
            df = database[database['region'].isin(region)]
    
        st.write(f'Records found:{len(df)}')     
        figure = get_location_interactive(df)
        st.plotly_chart(figure)
        st.markdown(df[['name', 'url', 'region', 'address']].sort_values(by=['name', 'region']).to_html(render_links=True),unsafe_allow_html=True)
        csv = df.to_csv(index=False).encode('utf-8')
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