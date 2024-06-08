import streamlit as st
from weather import *
from weatherchat import chatbot
from mapweather import *
from streamlit_folium import folium_static
from pikudhaorefalerts import *

# Initialize comparison data dictionary
comparison_data = {}

# Set page title and icon
st.set_page_config(page_title="Weather Comparison App", page_icon=":partly_sunny:")

# Custom CSS for background image and font color
page_bg_img = '''
<style>
.stApp {
  background: url("https://st.depositphotos.com/1013513/2753/i/450/depositphotos_27538253-stock-photo-heat-wave-in-the-city.jpg") no-repeat center center fixed;
  background-size: cover;
  color: black; /* Set font color to black */
}
button {
  background-color: blue !important;
}
.stButton>button {
  background-color: lightblue !important;
}
.stButton>button:hover {
  background-color: #0056b3 !important; /* Darker shade of blue on hover */
}
.sidebar .sidebar-content {
  color: orange;  /* Keep the sidebar font color as orange */
}
.css-1v3fvcr {
  color: black !important;  /* Force font color to black for the main content */
}
h1, h3, h4, h5, h6 {
  color: black !important;
}
h2 {
  color: orange !important;
}
.custom-command {
  color: black; /* Set font color to black for the custom commands */
  font-size: 20px; /* Adjust font size */
  font-weight: bold; /* Make text bold */
}
</style>
'''

# Apply custom CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Main title
st.title('Weather App')

# Sidebar menu options
st.sidebar.markdown("<h2 style='color: orange;'>Choose an option:</h2>", unsafe_allow_html=True)
menu_choice = st.sidebar.radio("", ["main", "Set Default Location", "Set Temperature Unit", "Compare Weather and Time",
                                    "Talk to Chatbot", "Show Map", "Pikud Haoref Alerts"])

# Main menu option
if menu_choice == "main":
    st.subheader("Welcome to weather application, have fun!!!")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://media0.giphy.com/media/ST16nmBERfkgyFGGk2/giphy.webp?cid=ecf05e47bhkzcazkabdsexsenqzc4dia0x27q3txyr4ywek4&ep=v1_gifs_search&rid=giphy.webp&ct=s", width=200)
    with col2:
        st.image("https://media4.giphy.com/media/7GUjGofrXN3t0GwUOW/giphy.webp?cid=790b7611ee6j3q8pijf83lkbawdebwk9prbbclfdl43wj6s7&ep=v1_gifs_search&rid=giphy.webp&ct=s", width=200)
    with col3:
        st.image("https://media2.giphy.com/media/EmqYqVb7vvgY4VzN9g/giphy.webp?cid=ecf05e47fg2kvntqikykcolu8jg4fe93cravt3qwoz6wibsp&ep=v1_gifs_search&rid=giphy.webp&ct=s", width=200)

# Set Default Location option
elif menu_choice == "Set Default Location":
    st.subheader("Set Default Location")
    st.write("Welcome! To set your default location, please provide the following information:")
    st.write("Example city - Paris, Country - France, Timezone - Europe/London")
    st.write("Example city - Tokyo, Country - Japan, Timezone - Asia/Tokyo")

    st.markdown("<div class='custom-command'>Enter your default city name:</div>", unsafe_allow_html=True)
    city_name = st.text_input("")
    st.markdown("<div class='custom-command'>Enter the country (optional):</div>", unsafe_allow_html=True)
    country_name = st.text_input(" ")
    st.markdown("<div class='custom-command'>Select the timezone:</div>", unsafe_allow_html=True)
    timezone_name = st.selectbox("",
                                 ["UTC", "Europe/London", "Asia/Jerusalem", "America/New_York", "America/Los_Angeles",
                                  "Asia/Tokyo", "Asia/Shanghai"])

    if st.button("Set Default Location"):
        result = set_default_location(city_name, country_name, timezone_name)
        st.success(result)

# Set Temperature Unit option
elif menu_choice == "Set Temperature Unit":
    st.subheader("Set Temperature Unit")
    st.markdown("<div class='custom-command'>Select your preferred temperature unit:</div>", unsafe_allow_html=True)
    unit = st.selectbox("", ["Celsius", "Fahrenheit"])

    if st.button("Set Temperature Unit"):
        result = set_temperature_unit(unit)
        st.success(result)

# Compare Weather and Time option
elif menu_choice == "Compare Weather and Time":
    st.subheader("Compare Weather and Time")
    st.markdown("<div class='custom-command'>Enter your default city name:</div>", unsafe_allow_html=True)
    city_name = st.text_input("")
    st.markdown("<div class='custom-command'>Enter the country (optional):</div>", unsafe_allow_html=True)
    country_name = st.text_input(" ")
    st.markdown("<div class='custom-command'>Select the timezone:</div>", unsafe_allow_html=True)
    user_timezone = st.selectbox("",
                                 ["UTC", "Europe/London", "Asia/Jerusalem", "America/New_York", "America/Los_Angeles",
                                  "Asia/Tokyo", "Asia/Shanghai"])

    if st.button("Compare Weather and Time"):
        default_city, default_country, default_timezone = get_default_location()
        comparison_data = compare_weather_and_time(default_city, default_country, default_timezone, city_name,
                                                   country_name, user_timezone)
        comparison_data['user_timezone'] = user_timezone

        if 'default_location' in comparison_data and 'user_location' in comparison_data:
            st.write("JSON Location:")
            st.markdown(
                f"""
                <div style="background-color: #90EE90; padding: 30px; border-radius: 20px; margin-bottom: 20px;">
                    <table style='border: none;'>
                        <tr>
                            <td style='width: 70%;'>
                                <h3>City: {comparison_data['default_location']['city']}</h3>
                                <p>Temperature: {comparison_data['default_location']['temperature']} °{get_temperature_unit()[0]}</p>
                                <p>Weather Conditions: {comparison_data['default_location']['weather_conditions']}</p>
                                <p>Humidity: {comparison_data['default_location']['humidity']}</p>
                                <p>Time: {comparison_data['default_location']['time']} {comparison_data['default_location']['timezone']}</p>
                            </td>
                            <td>
                                <img src="{display_weather_image(comparison_data['default_location']['temperature'])}" alt="Weather Icon" style="width:100px;">
                            </td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            st.write("User Location:")
            st.markdown(
                f"""
                <div style="background-color: #FF8488; padding: 30px; border-radius: 20px;">
                    <table style='border: none;'>
                        <tr>
                            <td style='width: 70%;'>
                                <h3>City: {comparison_data['user_location']['city']}</h3>
                                <p>Country: {comparison_data['user_location']['country']}</p>
                                <p>Temperature: {comparison_data['user_location']['temperature']} °{get_temperature_unit()[0]}</p>
                                <p>Weather Conditions: {comparison_data['user_location']['weather_conditions']}</p>
                                <p>Humidity: {comparison_data['user_location']['humidity']}</p>
                                <p>Time: {comparison_data['user_location']['time']} {comparison_data['user_location']['timezone']}</p>
                            </td>
                            <td>
                                <img src="{display_weather_image(comparison_data['user_location']['temperature'])}" alt="Weather Icon" style="width:100px;">
                            </td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Failed to retrieve comparison data.")

# Talk to Chatbot option
elif menu_choice == "Talk to Chatbot":
    st.subheader("Talk to Chatbot")
    st.write("Example questions the chatbot can answer:")
    st.markdown("- *What's the weather like in Paris?*")
    st.markdown("- *Is it sunny in London?*")
    st.markdown("- *How is the humidity in Tokyo?*")
    st.markdown("- *Is it cloudy in New York?*")
    st.markdown("- *Show all details for Berlin?*")
    st.markdown("###### Enter a city if the bot didn't know to answer")

    user_input = st.text_input("You:")
    if st.button("Send"):
        responses = chatbot(user_input)
        if responses:
            st.markdown(f"<p style='color: blue; font-size: 22px;'>Your question: {user_input}</p>", unsafe_allow_html=True)
            for response in responses:
                st.write("Bot:", response)
        else:
            st.write("Bot:", "Sorry, I didn't understand that.")

# Pikud Haoref Alerts option
elif menu_choice == "Pikud Haoref Alerts":
    _, merged_df_message = mainpikudorefalerts()
    st.markdown(" ")

    if isinstance(merged_df_message, pd.DataFrame):
        columns_to_display = ['alertDate', 'data', 'Temperature', 'Wind_Speed', 'Station_Name']
        for index, row in merged_df_message.iterrows():
            alert_date = row['alertDate']
            temperature = row['Temperature']
            wind_speed = row['Wind_Speed']
            station_name = row['Station_Name']
            typecat = row['title']
            title = f"<div style='text-align: right; color: #1a73e8; font-size: 24px; font-weight: bold;'> {typecat} - {alert_date}</div> <span style='color: #ea4335; font-size: 34px;'>{station_name}</span>"
            text = f"<div style='text-align: right; font-size: 20px;color: black;'> | טמפרטורה: {temperature} <span style='direction: rtl;'>&#8451;</span> | מהירות רוח: {wind_speed}</div>"
            image = ""
            if typecat == "חדירת כלי טיס עוין":
                image += f"<img src='https://cdn-icons-png.flaticon.com/128/10521/10521422.png' alt='Image' width='50' height='50'>"
            else:
                image += f"<img src='https://media4.giphy.com/media/daPKLhcdGhyD43LSKD/giphy.webp?cid=790b7611s3zk0896luynqww8znf6fphrrvz6kkhw4lr1eopq&ep=v1_gifs_search&rid=giphy.webp&ct=s' alt='Image' width='80' height='80'>"

            if float(temperature) > 30 or float(wind_speed) > 3:
                image += f"<div style='text-align: right; font-size: 18px; color: #ea4335;'> חשש לשרפות <img src='https://media4.giphy.com/media/sRW4SCnxfcx1LaFBtt/giphy.gif?cid=790b7611sk4zlitdgr9g68j1axxnj0f29iioq5fczeqdsqgj&ep=v1_stickers_search&rid=giphy.gif&ct=s' alt='Image' width='80' height='90'></div>"
            st.markdown(
                f"<div style='border-radius: 10px; border: 2px solid #e0e0e0; padding: 20px; margin: 20px; background-color:#D3D3D3;'>"
                f"<div>{title}</div>"
                f"<div>{image}</div>"
                f"<div>{text}</div>"
                f"</div>", unsafe_allow_html=True)
    else:
        st.write("Error occurred. Please check data fetching and merging.")

# Show Map option
else:
    st.subheader("Show Map")

    # Radio button to choose map display method
    map_display_option = st.radio("Choose Map Display Method", ["By JSON Data", "By City and Country"])

    if map_display_option == "By JSON Data":
        default_city, default_country, _ = get_default_location()
        m = city_location_map(default_city, default_country)
        if m:
            st.write("City Location Map:")
            st.write(f"City: {default_city}")
            st.write(f"Country: {default_country}")
            st_data = folium_static(m, height=370)
        else:
            st.error("Failed to generate map for the default location.")
            st.error("Check that city and country are not empty.")
            st.error("Change the JSON data in set_default_location function")
    else:
        dfcitycountry = read_city_data("data/worldcities.csv")

        # Dropdown lists for city and country
        cities = dfcitycountry['city'].unique()
        countries = dfcitycountry['country'].unique()

        # Dropdown lists for city and country
        city = st.selectbox("Select City", cities)
        country = st.selectbox("Select Country", countries)

        if st.button("Show City Location Map"):
            if city is not None and country is not None:
                m = city_location_map(city, country)
                if m:
                    st.write("City Location Map:")
                    st.write(f"City: {city}")
                    st.write(f"Country: {country}")
                    st_data = folium_static(m, height=370)
                else:
                    st.error(f"Failed to generate map for the selected - {city} - {country}.")
            else:
                st.error("City and country cannot be empty.")