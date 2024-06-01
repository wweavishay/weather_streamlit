import streamlit as st
from weather import *

# Set page title and icon
st.set_page_config(page_title="Weather Comparison App", page_icon=":partly_sunny:")

# Main title
st.title('Weather Comparison App')

# Main menu options
menu_choice = st.radio("Choose an option:", ["Set Default Location", "Set Temperature Unit", "Compare Weather and Time"])

if menu_choice == "Set Default Location":
    st.subheader("Set Default Location")
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
                st.write(f"Time: {comparison_data['default_location']['time']} {comparison_data['default_location']['timezone']}")
            with col2:
                st.image(display_weather_image(comparison_data['user_location']['temperature']), caption='Weather Icon')
        else:
            st.error("Failed to retrieve comparison data.")
