# Weather Streamlit Application

![Weather App](screenshot/welcome.png)

Welcome to the Weather Application! This command-line tool allows users to retrieve weather information, set default locations, compare weather conditions, receive alerts, and interact with a chatbot for weather-related queries.

## Overview

The Weather Application provides a range of functionalities to enhance users' experience in accessing weather data efficiently. Here are some key features:

- **Weather Information**: Get current weather conditions for any city around the world.
- **Default Location**: Set a default location for quick access to weather information.
- **Temperature Unit Preference**: Choose between Celsius and Fahrenheit for temperature display.
- **Comparative Analysis**: Compare weather conditions and time between different locations.
- **Alerts**: Receive alerts from the Home Front Command (Pikud Haoref) about various incidents, with a focus on predicting fires based on the location of the alarm, by analyzing temperature and wind conditions.
- **Map Visualization**: View a map showing the default location.
- **Chatbot Interaction**: Interact with a chatbot to inquire about weather conditions.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/weather-app.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Navigate to the local folder:

    ```bash
    cd weather_streamlit
    ```

4. Run the application:

    ```bash
    python main.py
    ```

## Usage

### Setting Default Location

To set a default location, use the CLI command:

```bash
python Cli.py set-default-location --city "CityName"
```

## Usage

### Setting Default Location


## CLI Commands

### Setting Temperature Unit

To set the temperature unit preference, use the following CLI commands:

```bash
python Cli.py set-temperature-unit --unit "Celsius/Fahrenheit"
python Cli.py set-temperature-unit --unit "Celsius"
```
<img src="screenshot/settemp.png" alt="Weather App" width="400">

- **Comparing Weather and Time**
```bash
python Cli.py compare-weather-and-time --city "CityName" --country "CountryName" --timezone "Timezone"

python Cli.py compare-weather-and-time --city "Paris" --country "France" --timezone "Europe/London"

```
<img src="screenshot/compare.png" alt="Weather App" width="400">

- **Talking to Chatbot**
```bash
python Cli.py talk-to-chatbot --user-input "Your question 

python Cli.py talk-to-chatbot --user-input "What's the weather like in Tokyo?"

```
<img src="screenshot/chatbot.png" alt="Weather App" width="400">

- **Pikud Haoref Alerts**
```bash
python Cli.py pikud-haoref-alerts 
```
<img src="screenshot/pikud haoref.png" alt="Weather App" width="400">

- **Showing Map**
```bash
python Cli.py show-map
```
<img src="screenshot/map.png" alt="Weather App" width="400">


#### website link - https://weatherapp-avishay-ak-barillan2024.streamlit.app/