# Browsing the AI Landscape in Belgium

In this project, we used the data available on the AI4Belgium website to build a dataset of the AI companies in the different regions of Belgium. 

The goal of this short project is to facilitate job seekers in finding AI companies close to their location. In particular, those who follow our AI training at [BeCode.org](www.becode.org). 

# Pipeline

1. Scrapping company name, website link, and region from AI4Belgium using BeautifulSoup
2. Scrapping company addresses from Google Search and Google Maps using Selenium
3. Visualize results in an interactive map using Plotly
4. Deploy on the web using Streamlit


# Further Improvements

* Further improvements would be to include the sectors and industry information to narrow down the search results. 
* Some companies have multiple locations which are unaccounted for.
* Include companies listed in other websites such as IMEC Start.

# Last Revised
August 26, 2022.

# Contributors
Made by Vanessa Rivera Quinones and Louis de Viron.