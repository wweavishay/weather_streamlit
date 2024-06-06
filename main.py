import streamlit as st
from weather import *
from weatherchat import chatbot
from historydata import *
from streamlit_folium import folium_static
from pikudhaorefalerts import *
comparison_data={}
# Set page title and icon
st.set_page_config(page_title="Weather Comparison App", page_icon=":partly_sunny:")

# Main title
st.title('Weather Comparison App')

# Main menu options
st.sidebar.markdown("<h1 style='color: orange;'>Choose an option:</h1>", unsafe_allow_html=True)
menu_choice = st.sidebar.radio("", ["Set Default Location", "Set Temperature Unit", "Compare Weather and Time", "Talk to Chatbot", "show map", "Pikud Haoref Alerts"])



if menu_choice == "Set Default Location":
    st.subheader("Set Default Location")
    # Instructions for new users
    st.write("Welcome! To set your default location, please provide the following information:")
    st.write("Example city - paris , Country - France ,Timezone - Europe/London  ")
    st.write("Example city - tokyo , Country - japan ,Timezone - Asia/Tokyo ")

    city_name = st.text_input("Enter your default city name:")
    country_name = st.text_input("Enter the country (optional):")
    timezone_name = st.selectbox("Select the timezone:", ["UTC", "Europe/London", "Asia/Jerusalem", "America/New_York", "America/Los_Angeles","Asia/Tokyo", "Asia/Shanghai"])

    if st.button("Set Default Location"):
        result = set_default_location(city_name, country_name, timezone_name)
        st.success(result)




elif menu_choice == "Set Temperature Unit":
    st.subheader("Set Temperature Unit")
    unit = st.selectbox("Select your preferred temperature unit:", ["Celsius", "Fahrenheit"])

    if st.button("Set Temperature Unit"):
        result = set_temperature_unit(unit)
        st.success(result)

elif menu_choice == "Compare Weather and Time":
    st.subheader("Compare Weather and Time")
    user_city = st.text_input("Enter user city name:")
    user_country = st.text_input("Enter user country name (optional):")
    user_timezone = st.selectbox("Select user timezone:",
                                 ["UTC", "Europe/London", "Asia/Jerusalem", "America/New_York", "America/Los_Angeles",
                                  "Asia/Tokyo", "Asia/Shanghai"])
    if st.button("Compare Weather and Time"):
        default_city, default_country, default_timezone = get_default_location()
        comparison_data = compare_weather_and_time(default_city, default_country, default_timezone, user_city,
                                                   user_country, user_timezone)
        comparison_data['user_timezone'] = user_timezone
        if comparison_data:
            # Display json location data
            st.write("JSON Location:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### City: {comparison_data['default_location']['city']}")
                st.write(f"Temperature: {comparison_data['default_location']['temperature']} °{get_temperature_unit()[0]}")
                st.write(f"Weather Conditions: {comparison_data['default_location']['weather_conditions']}")
                st.write(f"Humidity: {comparison_data['default_location']['humidity']}")
                st.write(
                    f"Time: {comparison_data['default_location']['time']} {comparison_data['default_location']['timezone']}")
            with col2:
                st.image(display_weather_image(comparison_data['default_location']['temperature']), caption='Weather Icon')

            # Display user location data
            st.write("--------------------------------------------------------------------")
            st.write("User Location:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### City: {comparison_data['user_location']['city']}")
                st.write(f"Country: {comparison_data['user_location']['country']}")
                st.write(f"Temperature: {comparison_data['user_location']['temperature']} °{get_temperature_unit()[0]}")
                st.write(f"Weather Conditions: {comparison_data['user_location']['weather_conditions']}")
                st.write(f"Humidity: {comparison_data['user_location']['humidity']}")
                st.write(f"Time: {comparison_data['user_location']['time']} {comparison_data['user_location']['timezone']}")
            with col2:
                st.image(display_weather_image(comparison_data['user_location']['temperature']), caption='Weather Icon')
        else:
            st.error("Failed to retrieve comparison data.")

elif menu_choice == "Talk to Chatbot":
    st.subheader("Talk to Chatbot")

    # Example questions the chatbot can answer
    st.write("Example questions the chatbot can answer:")
    st.markdown("- *What's the weather like in Paris?*")
    st.markdown("- *Is it sunny in London?*")
    st.markdown("- *How is the humidity in Tokyo?*")
    st.markdown("- *Is it cloudy in New York?*")
    st.markdown("- *Show all details for Berlin?*")
    st.markdown(" ######  Enter a city if the bot didn't know to answer ")
    st.markdown("  ")
    st.markdown("  ")
    user_input = st.text_input("You:")
    if st.button("Send"):
        responses = chatbot(user_input)
        if responses:
            st.markdown(f"<p style='color: yellow; font-size: 22px;'>Your question: {user_input}</p>", unsafe_allow_html=True)
            for response in responses:
                st.write("Bot:", response)  # Display chatbot's response
        else:
            st.write("Bot:", "Sorry, I didn't understand that.")

elif menu_choice == "Pikud Haoref Alerts":
    _, merged_df_message = mainpikudorefalerts()

    st.markdown(" ")

    # Check if merged_df_message is a DataFrame
    if isinstance(merged_df_message, pd.DataFrame):
        # Display rows of specific columns in a loop
        columns_to_display = ['alertDate', 'data', 'Temperature', 'Wind_Speed', 'Station_Name']
        for index, row in merged_df_message.iterrows():
            # Extract values from the row
            alert_date = row['alertDate']
            temperature = row['Temperature']
            wind_speed = row['Wind_Speed']
            station_name = row['Station_Name']
            typecat = row['title']  # טילים או כלי טייס עוין
            # Construct the text
            title = f"<div style='text-align: right; color: #1a73e8; font-size: 24px; font-weight: bold;'> {typecat} - {alert_date}</div> <span style='color: #ea4335; font-size: 34px;'>{station_name}</span>"
            text = f"<div style='text-align: right; font-size: 20px;color: black;'> | טמפרטורה: {temperature} <span style='direction: rtl;'>&#8451;</span> | מהירות רוח: {wind_speed}</div>"
            image = ""
            if typecat == "חדירת כלי טיס עוין":
                image += f"<img src='https://cdn-icons-png.flaticon.com/128/10521/10521422.png' alt='Image' width='50' height='50'>"
            else:
                image += f"<img src='https://cdn-icons-png.flaticon.com/128/1356/1356479.png' alt='Image' width='50' height='50'>"

            if float(temperature) > 30 or float(wind_speed) > 3:
                image += f"<div style='text-align: right; font-size: 18px; color: #ea4335;'> חשש לשרפות <img src='https://cdn-icons-png.flaticon.com/128/785/785116.png' alt='Image' width='50' height='50'></div>"
            # Enclose each row within a styled <div> element with a border
            st.markdown(f"<div style='border-radius: 10px; border: 2px solid #e0e0e0; padding: 20px; margin: 20px; background-color:#D3D3D3;'>"
                        f"<div>{title}</div>"
                        f"<div>{image}</div>"
                        f"<div>{text}</div>"
                        f"</div>", unsafe_allow_html=True)
    else:
        st.write("Error occurred. Please check data fetching and merging.")

else:
    st.subheader("Show Map")

    # Define default city and country
    default_city, default_country, _ = get_default_location()

    # Create a button for showing the map
    if st.button("Show City Location Map"):
        # Generate the map
        m = city_location_map(default_city.capitalize(), default_country.capitalize())

        # Check if the map was successfully generated
        if m:
            # Display map
            st.write("City Location Map:")
            st.write(f"City: {default_city}")
            st.write(f"Country: {default_country}")
            st_data = folium_static(m, height=370)

        else:
            st.error(f"Failed to generate map for the selected  -{default_city} - {default_country} .")