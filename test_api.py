
from utils.weather_utils import fetch_weather

def main():
	city = "Bhubaneswar"
	data = fetch_weather(city)
	print(data)


if __name__ == "__main__":
	main()
