import re

import requests
import pandas as pd
import xml.etree.ElementTree as ET
import json

def make_alert_df():
    url = "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        # If there's a problem fetching data, load from a local file
            with open("data/pikudoref.json", "r") as f:
                data = json.load(f)
            return pd.DataFrame(data)
    except ValueError as e:
        return f"Error creating DataFrame: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def xml_to_dataframe():
    url = "https://ims.gov.il/sites/default/files/ims_data/xml_files/imslasthour.xml"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            data = []
            for observation in root.findall('.//Observation'):
                observation_data = {}
                td_element = observation.find('TD')
                ws_element = observation.find('WS')
                stn_name_element = observation.find('stn_name')
                if td_element is not None and ws_element is not None and stn_name_element is not None:
                    observation_data['Temperature'] = td_element.text
                    observation_data['Wind_Speed'] = ws_element.text
                    observation_data['Station_Name'] = stn_name_element.text
                    data.append(observation_data)
            return pd.DataFrame(data)
        else:
            return f"Error: Unable to retrieve XML data. Status code: {response.status_code}. Attempting to load local data."
    except Exception as e:
        return f"An error occurred while fetching XML data: {e}. Attempting to load local data."

    # If retrieving data from URL fails, attempt to load from local file
    try:
        tree = ET.parse('data/weather.xml')  # Change the path as per your local file location
        root = tree.getroot()
        data = []
        for observation in root.findall('.//Observation'):
            observation_data = {}
            td_element = observation.find('TD')
            ws_element = observation.find('WS')
            stn_name_element = observation.find('stn_name')
            if td_element is not None and ws_element is not None and stn_name_element is not None:
                observation_data['Temperature'] = td_element.text
                observation_data['Wind_Speed'] = ws_element.text
                observation_data['Station_Name'] = stn_name_element.text
                data.append(observation_data)
        return pd.DataFrame(data)
    except Exception as e:
        return f"Error: Unable to load local XML data. {e}"

def read_excel_file():
    try:
        return pd.read_excel("data/yeshuvim.xlsx")
    except Exception as e:
        return f"An error occurred yeshuvim.xlsx: {e}"



def fetch_dataframes():
    df_alertoref = make_alert_df()
    df_weather = xml_to_dataframe()
    return df_alertoref, df_weather

def check_station_name(x, df_weather):
    if isinstance(x, str):
        for city in df_weather['Station_Name']:
            if city in x:
                return True
    return False

def merge_dataframes(df_alertoref, mapping_df, df_weather):
    if isinstance(df_alertoref, pd.DataFrame) and isinstance(mapping_df, pd.DataFrame):

        mapping_dict = mapping_df.set_index('englishcity')['hebrewcity'].to_dict()


        # Merge df_alertoref and
        # mapping_df on 'data' and 'hebrewcity' columns
        result_df = pd.merge(df_alertoref, mapping_df, how='left', left_on='data', right_on='hebrewcity')

        # Clean 'englishcity' column
        result_df['englishcity'] = result_df['englishcity'].apply(
            lambda x: re.sub(r'[^a-zA-Z]', '', str(x)) if isinstance(x, str) else x)

        if isinstance(df_weather, pd.DataFrame):
            # Perform the left join based on substring matching in both directions
            merged_df = pd.merge(result_df, df_weather, how='right',
                                 left_on=result_df['englishcity'].apply(check_station_name, args=(df_weather,)),
                                 right_on=df_weather['Station_Name'].apply(lambda x: any(
                                     station in x if isinstance(station, str) else False for station in
                                     result_df['englishcity'])))


            # Drop unnecessary columns resulting from the merge
            merged_df.drop(['key_0'], axis=1, inplace=True)

            # Remove duplicate rows based on 'Station_Name' column


            # Remove rows where 'Station_Name' or 'Wind_Speed' or 'Temperature' is NaN
            merged_df.dropna(subset=['Station_Name', 'Wind_Speed', 'Temperature'], axis=0, inplace=True)
            merged_df['Station_Name'] = merged_df['Station_Name'].map(mapping_dict)
            merged_df.drop_duplicates(subset=['Station_Name'], inplace=True)
            merged_df.dropna(subset=['Station_Name'], inplace=True)
            return merged_df
        else:
            return None
    else:
        return None


def mainpikudorefalerts():
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
    #print(alert_preview)
    print("---------MERGED----------")
    print(merged_df)

