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
        lat=df.lat,
        lon=df.lon,
        custom_data= [df['name'], df['url'] , df['street'], df['zip_code'], df['city']],
        color='region',
        color_continuous_scale=["green", 'blue', 'red', 'gold'],
        height=700,
        title='AI Landscape Belgium',
        opacity=.75,
       )
    
    fig.update_layout(mapbox_style=mapbox_style)
    fig.update_layout(margin={"r": 0, "l": 0, "b": 0})
    fig.update_traces(
    hovertemplate="<br>".join([
        "Name: %{customdata[0]}",
        "Website:  %{customdata[1]}",
        "Address: %{customdata[2]}",
        "City: %{customdata[3]}, %{customdata[4]}",
    ]))

    
    fig.update_geos(
    lataxis_range=[df.lat.min(), df.lat.max()],
    lonaxis_range=[df.lon.min(), df.lon.max()],
    ) 
    
    # Use Plotly's 'auto' bound fitting to center and zoom correctly
    fig.update_layout(
        mapbox=dict(
            # The bounds are set by the trace data by default when you remove zoom/center.
            # This line explicitly triggers the auto-fitting based on the traces.
            uirevision=True # Keeps the current map view when updating the plot
        )
    )
   
    return fig