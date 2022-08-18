import pandas as pd
import streamlit as st

# Define app using completed dataset
def main():
    st.title('Belgian AI Landscape')
    st.write('A list highlighting the companies focused on data science and artificial intelligence in Belgium.')

    region = st.text_input('Region', "")
    database = pd.read_csv('data/AI_Landscape_BE_complete.csv')

    if region != '':
        df = database[database['Region'] == region]
        st.dataframe(df)
  
if __name__ == '__main__':
    main()