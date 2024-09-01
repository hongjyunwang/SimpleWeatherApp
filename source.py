import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
from datetime import datetime
import pytz

# set up API call as global variables
API_KEY = "d5414be73d714712aeda1dc905698c87"
CURRENT_WEATHER_URL = "https://api.weatherbit.io/v2.0/current"
FORECAST_URL = "https://api.weatherbit.io/v2.0/forecast/daily"
ICON_URL = "https://www.weatherbit.io/static/img/icons/{}.png"

class WeatherApp:
    def __init__ (self, root):
        """
        Initialization of the WeatherApp class

        Inputs:
        - self: an instance of the class itself
        - root: an instance of a tk object that is the main application window 

        Outputs:
        None
        """
        # Characterize the main window root
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x430")
        self.root.resizable(False, False)

        # setup_ui member function is immediately called in WeatherApp initialization
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the basic graphics sections of the UI, including city input, the search button, and the data display

        Inputs:
        - self: an instance of the class itself

        Outputs:
        None
        """
        # City Input Box
        self.city_label = tk.Label(self.root, text = "Enter city:")
        self.city_label.pack(pady = 10)
        self.city_entry = tk.Entry(self.root, width = 30)
        self.city_entry.pack()

        # Search Button
        self.search_button = tk.Button(self.root, text = "Search", command = self.get_weather)
        self.search_button.pack(pady = 10)

        # Local Time Display
        self.local_time_label = tk.Label(self.root, font=("Arial", 14))
        self.local_time_label.pack(pady = 5)

        # Weather Information Display, including the frame and icon/temp/description/precipitation/wind labels
        self.weather_frame = tk.Frame(self.root)
        self.weather_frame.pack(pady = 20)

        self.icon_label = tk.Label(self.weather_frame)
        self.icon_label.grid(row = 0, column = 0, rowspan = 2)

        self.temp_label = tk.Label(self.weather_frame, font = ("Arial", 20))
        self.temp_label.grid(row = 0, column = 1, padx = 10)

        self.description_label = tk.Label(self.weather_frame)
        self.description_label.grid(row = 1, column = 1, padx = 10)

        self.precipitation_chance_label = tk.Label(self.root)
        self.precipitation_chance_label.pack()

        self.precipitation_amount_label = tk.Label(self.root)
        self.precipitation_amount_label.pack()

        self.wind_label = tk.Label(self.root)
        self.wind_label.pack()

        # Create a frame for the bottom elements
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side = tk.BOTTOM, fill = tk.X, pady = 10)

        # Configure grid columns
        self.bottom_frame.columnconfigure(0, weight = 1)  # Name column expands
        self.bottom_frame.columnconfigure(1, weight = 0)  # Info button column doesn't expand

        # Add my name
        self.name_label = tk.Label(self.bottom_frame, text = "Hong-Jyun Wang", font = ("Arial", 10))
        self.name_label.grid(row = 0, column = 0, sticky = "w", padx = 10)

        # Add info button
        self.info_button = tk.Button(self.bottom_frame, text = "ⓘ", command = self.show_info, font = ("Arial", 12))
        self.info_button.grid(row = 0, column = 1, sticky = "e", padx = 10)

    def get_local_time(self, timezone):
        """
        Get input city local time based on timezone

        Inputs:
        - self: instance of the class itself
        - timezone: timezone of the input city
        """
        local_time = datetime.now(pytz.timezone(timezone))
        return local_time.strftime("%I:%M %p")

    def get_weather(self):
        """
        Fetching the weather data from the API and updaing the UI, stores data in weather_data dictionary 

        Inputs:
        - self: an instance of the class itself

        Outputs:
        None
        """
        # Access city name from city_entry
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return
        
        params = {"city": city, "key": API_KEY, "units": "M"}

        try:
            current_weather = self.fetch_current_weather(city)
            forecast = self.fetch_forecast(city)

            # Update UI
            self.update_weather_display(current_weather, forecast[0])

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")

    def fetch_current_weather(self, city):
        """
        Access the current weather data through the CURRENT_WEATHER_URL

        Inputs:
        - self: instance of this class
        - city: inputted city name

        Outputs:
        None
        """
        params = {"city": city, "key": API_KEY, "units": "M"}
        response = requests.get(CURRENT_WEATHER_URL, params = params)
        response.raise_for_status()
        return response.json()['data'][0]
    
    def fetch_forecast(self, city):
        """
        Access the forecasted weather data through FORECAST_URL

        Inputs:
        - self: instance of this class
        - city: inputted city name

        Outputs:
        None
        """
        params = {"city": city, "key": API_KEY, "units": "M",  "days": 1}        
        response = requests.get(FORECAST_URL, params = params)
        response.raise_for_status()
        return response.json()['data']

    def show_info(self):
        """
        Command function for showing PM Accelerator information when info button is clicked
        
        Inputs:
        - self: an instance of the class itself
        """
        # Create a new window
        info_window = tk.Toplevel(self.root)
        info_window.title("About Weather App")
        info_window.geometry("300x200")

        # Add a text widget with a description
        info_text = tk.Text(info_window, wrap = tk.WORD, padx = 10, pady = 10)
        info_text.pack(expand = True, fill = tk.BOTH)
        
        description = """The Product Manager Accelerator Program is designed to support PM professionals 
        through every stage of their career. From students looking for entry-level jobs to Directors looking 
        to take on a leadership role, our program has helped over hundreds of students fulfill their career 
        aspirations. Our Product Manager Accelerator community are ambitious and committed. Through our program 
        they have learnt, honed and developed new PM and leadership skills, giving them a strong foundation for 
        their future endeavours."""
        
        info_text.insert(tk.END, description)
        info_text.config(state = tk.DISABLED)  # Make the text read-only

    def update_weather_display(self, current, forecast):
        """
        Updates the UI display based on the data accessed from the API

        Inputs:
        - self: an instance of the class itself
        - current: Current weather data obtained from API call
        - forecast: Forecasted weather data obtained from API call

        Outputs:
        None
        """
        # Extract necessary values from fetched current and forecast data
        temp = current['temp']
        description = current['weather']['description']
        icon_code = current['weather']['icon']
        wind_speed = current['wind_spd']
        precip_amount = current['precip']
        precip_chance = forecast['pop']
        timezone = current['timezone']

        # Get local time
        local_time = self.get_local_time(timezone)

        # Update labels
        self.local_time_label.config(text=f"Local Time: {local_time}")
        self.temp_label.config(text = f"{temp}°C")
        self.description_label.config(text = description)
        self.precipitation_chance_label.config(text=f"Chance of Precipitation: {precip_chance}%")
        self.precipitation_amount_label.config(text = f"Amount of precipitation: {precip_amount} mm")
        self.wind_label.config(text = f"Wind speed: {wind_speed} m/s")

        # Fetch and display weather icon
        icon_url = ICON_URL.format(icon_code)
        try:
            response = requests.get(icon_url)
            response.raise_for_status()
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            photo = ImageTk.PhotoImage(img)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo
        except requests.RequestException:
            self.icon_label.config(image = "")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()