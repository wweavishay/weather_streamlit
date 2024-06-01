import pandas as pd
import folium



def city_location_map(city=None, country=None):
    file = "worldcities.csv"
    data = pd.read_csv(file)

    if city is not None and country is not None:
        # Both city and country are provided
        country_data = data.loc[(data["country"] == country) & (data["city_ascii"] == city)]
    elif city is not None:
        # Only city is provided
        country_data = data.loc[data["city_ascii"] == city]
    elif country is not None:
        # Only country is provided
        country_data = data.loc[data["country"] == country]
    else:
        return None  # Neither city nor country is provided

    if country_data.empty:
        return None  # City not found in the specified country

    lat = float(country_data["lat"])
    lng = float(country_data["lng"])

    # Create a folium map and add a marker for the city
    m = folium.Map(location=[lat, lng], zoom_start=7)
    folium.Marker([lat, lng],
                  popup=city + ', ' + country,
                  tooltip=city + ', ' + country).add_to(m)

    return m







