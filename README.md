# Browsing the AI Landscape in Belgium

In this project, we used the data available on the AI4Belgium website to build a dataset of the AI companies in the different regions of Belgium. 

The goal of this short project is to facilitate job seekers (in particular, those who follow our AI training at [BeCode.org](www.becode.org)) in finding AI companies close to their location where they could potentially apply for jobs or internships.

# Pipeline

1. First, we scrape company name, website link, and region from AI4Belgium using BeautifulSoup. We save the data as a CSV file. 
2. Then, we find and scrape company addresses from Google Search and Google Maps using Selenium. 
3. We use the addresses to geocode the locations using the OpenStreeMap API and visualize results in an interactive map using Plotly.
4. Finally, we deploy on the web using Streamlit. You can navigate to the app using this link: [https://ai-landscape-be.streamlit.app/](https://ai-landscape-be.streamlit.app/).

Note: For some companies, we couldn't scrape the address we manually imputed the data. 

# Further Improvements

* Further improvements would be to include the sectors and industry information to narrow down the search results. 
* Some companies have multiple locations which are unaccounted for.
* Include start-up listed in other websites such as IMEC Start.

# Last Revised
August 26, 2022.

# Contributors
Made by Vanessa Rivera Quinones and Louis de Viron.