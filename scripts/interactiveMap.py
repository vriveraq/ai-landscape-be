import plotly.express as px

def get_location_interactive(df, mapbox_style="open-street-map"):
    """Return a map with markers for houses based on lat and long.
    
    Parameters:
    ===========
    mapbox_style = str; options are following:
        > "white-bg" yields an empty white canvas which results in no external HTTP requests
        > "carto-positron", "carto-darkmatter", "stamen-terrain",
          "stamen-toner" or "stamen-watercolor" yield maps composed of raster tiles 
          from various public tile servers which do not require signups or access tokens
        > "open-street-map" does work 'latitude', 'longitude'
    """
    fig = px.scatter_mapbox(
        df,
        lat=df.Latitude,
        lon=df.Longitude,
        custom_data= [df['Company Name'], df['Link'] , df['Address']],
        color='Region',
        color_continuous_scale=["green", 'blue', 'red', 'gold'],
        zoom=11.5,
        height=700,
        title='AI Landscape',
        opacity=.5,
        center={
            'lat': df.Latitude.mode()[0],
            'lon': df.Longitude.mode()[0]
        })
    fig.update_layout(mapbox_style=mapbox_style)
    fig.update_layout(margin={"r": 0, "l": 0, "b": 0})
    fig.update_traces(
    hovertemplate="<br>".join([
        "Name: %{customdata[0]}",
        "Website: %{customdata[1]}",
        "Address: %{customdata[2]}",
    ])
)
   
    return fig