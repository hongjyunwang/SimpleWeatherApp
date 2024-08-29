import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

class WeatherApp:
    def __init__ (self, root):
        """
        Initialization of the WeatherApp class

        Inputs:
        self: an instance of the class itself
        root: an instance of a tk object that is the main application window 

        Outputs:
        None
        """
        # Characterize the main window root
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # set up API call
        self.api_key = "8bb3b954b2e187cdb9316774b94f260c"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

        # setup_ui member function is immediately called in WeatherApp initialization
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the basic graphics sections of the UI, including city input, the search button, and the data display

        Inputs:
        self: an instance of the class itself

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

        # Weather Information Display, including the frame and icon/temp/description/precipitation/wind labels
        self.weather_frame = tk.Frame(self.root)
        self.weather_frame.pack(pady = 20)

        self.icon_label = tk.Label(self.weather_frame)
        self.icon_label.grid(row = 0, column = 0, rowspan = 2)

        self.temp_label = tk.Label(self.weather_frame, font = ("Arial", 20))
        self.temp_label.grid(row = 0, column = 1, padx = 10)

        self.description_label = tk.Label(self.weather_frame)
        self.description_label.grid(row = 1, column = 1, padx = 10)

        self.precipitation_label = tk.Label(self.root)
        self.precipitation_label.pack()

        self.wind_label = tk.Label(self.root)
        self.wind_label.pack()

    # Needs to define get_weather function
    def get_weather():
        return

    


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()