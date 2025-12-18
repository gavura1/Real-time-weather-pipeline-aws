from clients.weather_api import fetch_current_weather


def main() -> None:
    city = "Banska Bystrica"

    result = fetch_current_weather(city)

    print("Raw result from fetch_current_weather:")
    print(result)

    if result is not None:
        try:
            print("\nAs dict:")
            print(result.model_dump())
        except AttributeError:
            
            pass


if __name__ == "__main__":
    main()
