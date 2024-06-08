import pandas as pd
import folium


def read_city_data(file):
    """Reads the city data from a CSV file and returns it as a DataFrame."""
    return pd.read_csv(file)


def get_country_data(data, city, country):
    """Fetches data for the specified city and country from the DataFrame."""
    return data.loc[(data["country"] == country) & (data["city_ascii"] == city)]


def get_city_data(data, city):
    """Fetches data for the specified city from the DataFrame."""
    return data.loc[data["city_ascii"] == city]


def get_country_only_data(data, country):
    """Fetches data for the specified country from the DataFrame."""
    return data.loc[data["country"] == country]


def get_location_data(data, city, country):
    """Gets location data based on provided city and country."""
    if city is not None and country is not None:
        return get_country_data(data, city, country)
    elif city is not None:
        return get_city_data(data, city)
    elif country is not None:
        return get_country_only_data(data, country)
    else:
        return None


def create_map(lat, lng, city, country):
    """Creates a folium map centered at the specified latitude and longitude."""
    m = folium.Map(location=[lat, lng], zoom_start=7)
    folium.Marker(
        [lat, lng],
        popup=f"{city}, {country}",
        tooltip=f"{city}, {country}"
    ).add_to(m)
    return m


def city_location_map(city=None, country=None):
    """Creates a folium map for the specified city and country."""
    file = "data/worldcities.csv"
    data = read_city_data(file)

    location_data = get_location_data(data, city, country)
    if location_data is None or location_data.empty:
        return None  # City or country not found

    lat = float(location_data["lat"])
    lng = float(location_data["lng"])

    return create_map(lat, lng, city, country)


if __name__ == "__main__":
    # Example usage
    map_object = city_location_map(city="TOKYO", country="JAPAN")

