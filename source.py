import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
from datetime import datetime
import pytz
import math

# set up API call as global variables
API_KEY = "68b6c8b34e0b43bdb5be7a296e63d229"
CURRENT_WEATHER_URL = "https://api.weatherbit.io/v2.0/current"
DAILY_FORECAST_URL = "https://api.weatherbit.io/v2.0/forecast/daily"
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
        self.root.geometry("1000x700")
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
        self.city_label = tk.Label(self.root, text = "Enter Country/District/City/Street:")
        self.city_label.pack(pady = 10)
        self.city_entry = tk.Entry(self.root, width = 30)
        self.city_entry.pack()

        # Search Button
        self.search_button = tk.Button(self.root, text = "Search", command = self.get_weather)
        self.search_button.pack(pady = 10)

         # Bind the Enter key to the city entry
        self.city_entry.bind('<Return>', self.get_weather)

        # Local Time Display
        self.local_time_label = tk.Label(self.root, font=("Arial", 14))
        self.local_time_label.pack(pady = 5)

        # Weather Information Display, including the frame and icon/temp/description/precipitation/wind labels
        self.weather_frame = tk.Frame(self.root)
        self.weather_frame.pack(pady = 20)

        self.icon_label = tk.Label(self.weather_frame)
        self.icon_label.grid(row = 0, column = 0, rowspan = 2)

        self.temp_frame = tk.Frame(self.weather_frame)
        self.temp_frame.grid(row=0, column=1, padx=10)

        self.temp_c_label = tk.Label(self.temp_frame, font=("Arial", 20))
        self.temp_c_label.pack(side=tk.LEFT)

        self.temp_f_label = tk.Label(self.temp_frame, font=("Arial", 20))
        self.temp_f_label.pack(side=tk.LEFT, padx=(10, 0))

        self.description_label = tk.Label(self.weather_frame)
        self.description_label.grid(row = 1, column = 1, padx = 10)

        self.precipitation_chance_label = tk.Label(self.root)
        self.precipitation_chance_label.pack()

        self.precipitation_amount_label = tk.Label(self.root)
        self.precipitation_amount_label.pack()

        self.wind_label = tk.Label(self.root)
        self.wind_label.pack()

        # Daily Forecast Display
        self.daily_frame = tk.Frame(self.root)
        self.daily_frame.pack(pady = 20, padx = 10, fill = tk.X)

        self.daily_label = tk.Label(self.daily_frame, text = "7-Day Forecast", font = ("Arial", 14, "bold"))
        self.daily_label.pack()

        self.daily_canvas = tk.Canvas(self.daily_frame, height = 150)
        self.daily_canvas.pack(fill = tk.X)

        self.daily_scroll = tk.Scrollbar(self.daily_frame, orient = tk.HORIZONTAL, command = self.daily_canvas.xview)
        self.daily_scroll.pack(fill = tk.X)

        self.daily_canvas.configure(xscrollcommand = self.daily_scroll.set)
        self.daily_canvas.bind('<Configure>', lambda e: self.daily_canvas.configure(scrollregion = self.daily_canvas.bbox("all")))

        self.daily_inner_frame = tk.Frame(self.daily_canvas)
        self.daily_canvas.create_window((0, 0), window = self.daily_inner_frame, anchor = "nw")

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

    def get_weather(self, event=None):
        """
        Fetching the weather data from the API and updaing the UI, stores data in weather_data dictionary 

        Inputs:
        - self: an instance of the class itself
        - event: the event that triggered this method (optional, used for key bindings)

        Outputs:
        None
        """
        # Access city name from city_entry
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return
        
        try:
            current_weather = self.fetch_current_weather(city)

            forecast = self.fetch_daily_forecast(city)

            daily_forecast = self.fetch_daily_forecast(city)

            # Update UI
            self.update_weather_display(current_weather, forecast[0])
            self.update_daily_forecast_display(daily_forecast)

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
    
    def fetch_daily_forecast(self, city):
        """
        Access the forecasted weather data through DAILY_FORECAST_URL

        Inputs:
        - self: instance of this class
        - city: inputted city name

        Outputs:
        None
        """
        params = {"city": city, "key": API_KEY, "units": "M",  "days": 7}        
        response = requests.get(DAILY_FORECAST_URL, params = params)
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
        info_window.geometry("700x200")

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
        temp_c = current['temp']
        temp_f = (temp_c * 9/5) + 32
        description = current['weather']['description']
        icon_code = current['weather']['icon']
        wind_speed_m_s = current['wind_spd']
        wind_speed_ft_s = wind_speed_m_s * 3.28084
        precip_amount = math.trunc(current['precip'])
        precip_chance = forecast['pop']
        timezone = current['timezone']

        # Get local time
        local_time = self.get_local_time(timezone)

        # Update labels
        self.local_time_label.config(text=f"Local Time: {local_time}", font = ("Arial", 20))
        self.temp_c_label.config(text = f"{temp_c:.1f}°C", font = ("Arial", 20))
        self.temp_f_label.config(text = f"({temp_f:.1f}°F)", font = ("Arial", 20))
        self.description_label.config(text = description, font = ("Arial", 20))
        self.precipitation_chance_label.config(text = f"Chance of Precipitation: {precip_chance}%")
        self.precipitation_amount_label.config(text = f"Amount of Precipitation: {precip_amount} mm")
        self.wind_label.config(text = f"Wind Speed: {wind_speed_m_s:.1f} m/s ({wind_speed_ft_s:.1f} ft/s)")

        # Fetch and display weather icon
        icon_url = ICON_URL.format(icon_code)
        try:
            response = requests.get(icon_url)
            response.raise_for_status()
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            photo = ImageTk.PhotoImage(img)
            self.icon_label.config(image = photo)
            self.icon_label.image = photo
        except requests.RequestException:
            self.icon_label.config(image = "")

    def update_daily_forecast_display(self, forecast):
        # Clear any previous forecast data
        for widget in self.daily_inner_frame.winfo_children():
            widget.destroy()

        # Create a new frame to hold the forecast widgets and center it
        forecast_holder = tk.Frame(self.daily_inner_frame)
        forecast_holder.grid(row=0, column=0, padx=20, pady=10)
        
        # Check if forecast data exists
        if not forecast:
            tk.Label(forecast_holder, text="No Forecast Data Available.").pack()
            return

        # Loop through each day's forecast and create the UI elements
        for i, day_data in enumerate(forecast):
            day_frame = tk.Frame(forecast_holder)
            day_frame.grid(row=0, column=i, padx=15, pady=5, sticky="n")
            
            # Date Label
            date = datetime.strptime(day_data['valid_date'], "%Y-%m-%d")
            date_label = tk.Label(day_frame, text=date.strftime("%a\n%d/%m"))
            date_label.pack()

            # Weather Icon
            icon_code = day_data['weather']['icon']
            icon_url = ICON_URL.format(icon_code)
            try:
                response = requests.get(icon_url)
                response.raise_for_status()
                img_data = response.content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((30, 30), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                icon_label = tk.Label(day_frame, image = photo)
                icon_label.image = photo
                icon_label.pack()
            except requests.RequestException:
                icon_label = tk.Label(day_frame, text = "No Icon")
                icon_label.pack()

            # Precipitation Chance Label
            precip_chance = day_data['pop']
            precip_label = tk.Label(day_frame, text = f"{precip_chance}%")
            precip_label.pack()

            # Temperature Label
            temp_c = day_data['temp']
            temp_f = (temp_c * 9/5) + 32
            temp_label = tk.Label(day_frame, text=f"{temp_c:.1f}°C ({temp_f:.1f}°F)")
            temp_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()