import argparse
from weather import *
from weatherchat import chatbot
from mapweather import *
from pikudhaorefalerts import *

def set_default_location_command(args):
    """Sets the default location (city, country, and timezone) for weather information."""
    city_name = args.city
    country_name = args.country
    timezone_name = args.timezone
    if not city_name:  # Check if city_name is empty or None
        city_name = input("Enter your default city name: ")
    if not timezone_name:  # Check if timezone_name is empty or None
        timezone_name = input("Select the timezone: ")
    if not country_name and not args.country:  # Check if country_name is empty or None and args.country is not provided
        country_name = input("Enter the country (optional): ")
    result = set_default_location(city_name, country_name, timezone_name)
    print(result)

def set_temperature_unit_command(args):
    """Sets the preferred temperature unit (Celsius or Fahrenheit)."""
    unit = args.unit
    if not unit:
        unit = input("Select your preferred temperature unit (Celsius/Fahrenheit): ")
    result = set_temperature_unit(unit)
    print(result)

def compare_weather_and_time_command(args):
    """Compares the weather and time between the user's location and another specified location."""
    city_name = args.city
    country_name = args.country
    user_timezone = args.timezone
    if not city_name:
        city_name = input("Enter your default city name: ")
    if not country_name:
        country_name = input("Enter the country (optional): ")
    if not user_timezone:
        user_timezone = input("Select your timezone: ")
    comparison_data = compare_weather_and_time(city_name, country_name, user_timezone)
    # Display comparison_data here

def talk_to_chatbot_command(args):
    """Interacts with a chatbot to get weather-related responses."""
    user_input = args.user_input
    if not user_input:
        user_input = input("You: ")
    responses = chatbot(user_input)
    if responses:
        for response in responses:
            print(f"Bot: {response}")
    else:
        print("Bot: Sorry, I didn't understand that.")

def pikud_haoref_alerts_command(args):
    """Fetches and displays Pikud Haoref alerts."""
    _, merged_df_message = mainpikudorefalerts()
    # Display merged_df_message here

def show_map_command(args):
    """Shows a map with the user's default city location highlighted."""
    default_city, default_country, _ = get_default_location()
    if default_city and default_country:
        m = city_location_map(default_city.capitalize(), default_country.capitalize())
        # Display map here
    else:
        print("Error: Default location not set.")

def main():
    """Main function to parse command-line arguments and invoke corresponding functions."""
    parser = argparse.ArgumentParser(description="Weather Application CLI")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Define subparsers for each command
    parser_set_default_location = subparsers.add_parser("set-default-location", help="Set default location")
    parser_set_default_location.add_argument("--city", help="Enter your default city name")
    parser_set_default_location.add_argument("--country", help="Enter the country (optional)")
    parser_set_default_location.add_argument("--timezone", help="Select the timezone")
    parser_set_default_location.set_defaults(func=set_default_location_command)

    parser_set_temperature_unit = subparsers.add_parser("set-temperature-unit", help="Set temperature unit")
    parser_set_temperature_unit.add_argument("--unit", help="Select your preferred temperature unit (Celsius/Fahrenheit)")
    parser_set_temperature_unit.set_defaults(func=set_temperature_unit_command)

    parser_compare_weather_and_time = subparsers.add_parser("compare-weather-and-time", help="Compare weather and time")
    parser_compare_weather_and_time.add_argument("--city", help="Enter your default city name")
    parser_compare_weather_and_time.add_argument("--country", help="Enter the country (optional)")
    parser_compare_weather_and_time.add_argument("--timezone", help="Select your timezone")
    parser_compare_weather_and_time.set_defaults(func=compare_weather_and_time_command)

    parser_talk_to_chatbot = subparsers.add_parser("talk-to-chatbot", help="Talk to Chatbot")
    parser_talk_to_chatbot.add_argument("--user-input", help="User input for the chatbot")
    parser_talk_to_chatbot.set_defaults(func=talk_to_chatbot_command)

    parser_pikud_haoref_alerts = subparsers.add_parser("pikud-haoref-alerts", help="Pikud Haoref Alerts")
    parser_pikud_haoref_alerts.set_defaults(func=pikud_haoref_alerts_command)

    parser_show_map = subparsers.add_parser("show-map", help="Show Map")
    parser_show_map.set_defaults(func=show_map_command)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
