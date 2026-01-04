import customtkinter as ctk
from ui.controller import Controller

class loginWindow(ctk.CTkFrame):
    def __init__(self, master , controller : Controller, **kwargs):
        super().__init__(master)
        self.controller = controller
        # Add login widgets (e.g., entries, buttons) here
        # Example: Username entry
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter username")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter password", show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_action)
        self.login_button.pack(pady=10)

    def login_action(self):
        # Add your login logic here (e.g., check credentials)
        username = self.username_entry.get()
        username = username[1:] if username.startswith("0") else username
        password = self.password_entry.get()
        success = self.controller.login(username, password)
        if success:
            print("Login successful")
        else:
            print("Login failed")