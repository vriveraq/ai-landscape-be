import os
import pandas as pd
import streamlit as st
from interactiveMap import get_location_interactive

# Define app using completed dataset
def main():
    st.title('Belgian AI Landscape')
    st.write('A list highlighting the companies focused on data science and artificial intelligence in Belgium.')

    region = st.multiselect(
     'Regions:',
     ['Brussels', 'Flanders', 'Wallonia'],
     ['Brussels', 'Flanders', 'Wallonia'])
    filepath = os.path.join(os.path.dirname(__file__), "data/AILandscape_geocoded.csv")
    database = pd.read_csv(filepath)

    if region != '':
        df = database[database['Region'].isin(region)]
      
        figure = get_location_interactive(df)
        st.plotly_chart(figure)
        st.dataframe(df)

        csv = df.to_csv().encode('utf-8')
        st.download_button(
                "Press to Download",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
                )

  
if __name__ == '__main__':
    main()