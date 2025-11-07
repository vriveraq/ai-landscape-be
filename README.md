# Browsing the AI Landscape in Belgium
[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


In this project, we used the data available on the [AI4Belgium](https://bosa.belgium.be/nl/AI4Belgium/observatorium) website to build a dataset of the AI companies in the different regions of Belgium. 

The goal of this short project is to facilitate job seekers (in particular, those who follow our AI training at [BeCode.org](www.becode.org)) in finding AI companies close to their location where they could potentially apply for jobs or internships.

## 📦 Repo structure
```
.
├── data/
│   ├── old_data/
│   ├── raw_scraped_dataset.csv
│   ├── clean_scraped_dataset.csv
│   └── geocoded_dataset.csv
├── scripts/
├── testing/
├── .gitignore
├── app.py
└── README.md
````

## 🛎️ Usage
1. Clone the repository to your local machine.
2. Install requirements

    ```pip install -r requirements.txt```
3. To run app locally, run in terminal:

    ``` streamlit run app.py```

## 🤖 Pipeline

1. First, we scrape company name, website, category, region, logo, and creation year from AI4Belgium using Selenium and save the data as a CSV file. 
2. Then, we find and scrape company addresses from [CBE Public Search](https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html) website.
3. We use Geopy to geocode the locations using the OpenStreeMap API and visualize results in an interactive map using Plotly.
4. Finally, we deploy on the web using Streamlit. You can navigate to the app using this link: [https://ai-landscape-be.streamlit.app/](https://ai-landscape-be.streamlit.app/).

Note: Companies with no available information in CBE website where excluded from the dataset.

## 🏋️‍♀️Further Improvements
* Some companies may have multiple locations which are unaccounted for.
* Implement multi-threading to speed up processing time
* Include start-up listed in other websites such as IMEC Start and DigitalWallonia
* Give the option for the user to check available employment opportunities
* Implement an LLM that can answer questions about the companies in the dataset



![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)
 Let's connect: https://www.linkedin.com/in/vriveraq/

#### Last Revised: November 05, 2025