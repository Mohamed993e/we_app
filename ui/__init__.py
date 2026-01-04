from ui.controller import Controller
import customtkinter as ctk
from typing import Any, Callable

class MainView(ctk.CTkFrame):
    def __init__(self, master=None ,dismiss_callback : Callable[[], Any]=None, **kwargs):
        super().__init__(master , **kwargs)  # Initialize the CTkFrame parent class
        self.controller = Controller(view=self , dismiss_callback=dismiss_callback)
        self.pack(padx=2, pady=2, expand=True, fill="both")

