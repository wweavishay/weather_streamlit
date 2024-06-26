import re
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import json


def read_excel_file():
    """Reads the Excel file containing city mappings. Returns a DataFrame or an error message if reading fails."""
    try:
        return pd.read_excel("data/yeshuvim.xlsx")
    except Exception as e:
        return f"An error occurred while reading yeshuvim.xlsx: {e}"


def fetch_dataframes():
    """Fetches alert and weather dataframes by calling respective functions."""
    df_alertoref = make_alert_df()
    df_weather = xml_to_dataframe()
    return df_alertoref, df_weather


def contains_substring(s1, s2):
    """Checks if one string contains the other. Returns True if so, False otherwise."""
    s1 = str(s1)
    s2 = str(s2)
    return s1 in s2 or s2 in s1


def make_alert_df():
    """Fetches alert data from a remote JSON source and returns it as a DataFrame.
    If fetching fails, it loads the data from a local file."""
    url = "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        return load_local_alert_data(e)
    except ValueError as e:
        print(f"Error creating DataFrame: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def load_local_alert_data(error):
    """Loads alert data from a local JSON file if fetching from the URL fails."""
    print(f"Error fetching data from URL: {error}")
    with open("data/pikudoref.json", "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)


def xml_to_dataframe():
    """Fetches weather data from a remote XML source and returns it as a DataFrame.
    If fetching fails, it loads the data from a local file."""
    url = "https://ims.gov.il/sites/default/files/ims_data/xml_files/imslasthour.xml"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return parse_xml_data(response.content)
        else:
            return f"Error: Unable to retrieve XML data. Status code: {response.status_code}. Attempting to load local data."
    except Exception as e:
        return f"An error occurred while fetching XML data: {e}. Attempting to load local data."


def parse_xml_data(xml_content):
    """Parses XML data and returns it as a DataFrame."""
    root = ET.fromstring(xml_content)
    data = []
    for observation in root.findall('.//Observation'):
        observation_data = extract_observation_data(observation)
        if observation_data:
            data.append(observation_data)
    return pd.DataFrame(data)


def extract_observation_data(observation):
    """Extracts data from an XML observation element."""
    td_element = observation.find('TD')
    ws_element = observation.find('WS')
    stn_name_element = observation.find('stn_name')
    if td_element is not None and ws_element is not None and stn_name_element is not None:
        return {
            'Temperature': td_element.text,
            'Wind_Speed': ws_element.text,
            'Station_Name': stn_name_element.text
        }
    return None


def load_local_xml_data():
    """Loads weather data from a local XML file if fetching from the URL fails."""
    try:
        tree = ET.parse('data/weather.xml')
        root = tree.getroot()
        data = []
        for observation in root.findall('.//Observation'):
            observation_data = extract_observation_data(observation)
            if observation_data:
                data.append(observation_data)
        return pd.DataFrame(data)
    except Exception as e:
        return f"Error: Unable to load local XML data. {e}"


def merge_dataframes(df_alertoref, mapping_df, df_weather):
    """Merges alert and weather DataFrames using city name mappings.
    Returns the merged DataFrame or None if merging fails."""
    if isinstance(df_alertoref, pd.DataFrame) and isinstance(mapping_df, pd.DataFrame):
        df_alertoref['data'] = map_city_names(df_alertoref, mapping_df)
        clean_city_names(df_alertoref)
        if isinstance(df_weather, pd.DataFrame):
            merged_df = merge_alert_and_weather(df_alertoref, df_weather)
            return finalize_merged_df(merged_df, mapping_df)
        else:
            return None
    else:
        return None


def map_city_names(df_alertoref, mapping_df):
    """Maps Hebrew city names to English using the mapping DataFrame."""
    mapping_dict = mapping_df.set_index('hebrewcity')['englishcity'].to_dict()
    return df_alertoref['data'].map(mapping_dict)


def clean_city_names(df_alertoref):
    """Cleans the 'data' column in the alert DataFrame."""
    df_alertoref['data'] = df_alertoref['data'].apply(
        lambda x: re.sub(r'[^a-zA-Z]', '', str(x)) if isinstance(x, str) else x
    )


def merge_alert_and_weather(df_alertoref, df_weather):
    """Merges alert and weather DataFrames on city names."""
    return pd.merge(
        df_alertoref, df_weather, how='inner',
        left_on=df_alertoref['data'].apply(lambda x: x if any(
            contains_substring(x, y) for y in df_weather['Station_Name']) else None),
        right_on=df_weather['Station_Name'].apply(lambda x: x if any(
            contains_substring(x, y) for y in df_alertoref['data']) else None)
    )


def finalize_merged_df(merged_df, mapping_df):
    """Finalizes the merged DataFrame by mapping back city names to Hebrew and cleaning up."""
    mapping_dicthe = mapping_df.set_index('englishcity')['hebrewcity'].to_dict()
    merged_df['Station_Name'] = merged_df['data'].map(mapping_dicthe)
    merged_df.dropna(subset=['Station_Name', 'Wind_Speed', 'Temperature'], axis=0, inplace=True)
    merged_df.drop_duplicates(subset=['Station_Name'], inplace=True)
    merged_df.dropna(subset=['Station_Name'], inplace=True)
    return merged_df


def mainpikudorefalerts():
    """Main function to fetch, merge, and preview alert and weather data."""
    df_alertoref, df_weather = fetch_dataframes()
    mapping_df = read_excel_file()
    if mapping_df is None:
        return None, "Error reading mapping DataFrame."

    merged_df = merge_dataframes(df_alertoref, mapping_df, df_weather)

    if merged_df is None:
        return None, "Error merging dataframes."
    else:
        alert_preview = df_alertoref if not df_alertoref.empty else "No data available in Alert DataFrame."
        print("------------")
        print(alert_preview)
        return alert_preview, merged_df


if __name__ == "__main__":
    alert_preview, merged_df = mainpikudorefalerts()
    # print(alert_preview)
    # print(merged_df)
