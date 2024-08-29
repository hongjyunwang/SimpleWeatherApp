import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

class WeatherApp:
    def __init__ (self, root):
        """
        Initialization of the WeatherApp class

        self: an instance of the class itself
        root: an instance of a tk object that is the main application window 
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

    