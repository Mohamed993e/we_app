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
         # 1. Change UI to loading state
        self.login_button.configure(text="Loading...", state="disabled", cursor="wait")

        # 2. FORCE the UI to redraw immediately!
        self.update_idletasks() 
        try:

            # Add your login logic here (e.g., check credentials)
            username = self.username_entry.get()
            username = username[1:] if username.startswith("0") else username
            password = self.password_entry.get()
            success = self.controller.login(username, password)
            if success:
                print("Login successful")
            else:
                print("Login failed")
        except Exception as e:
            print(f"Error during login: {e}")
            self.login_button.configure(text="Login", state="normal", cursor="arrow")
        finally:
            # 4. Restore UI state (This runs even if there is an error)
            self.login_button.configure(text="Login" , state="normal", cursor="arrow")
            self.update_idletasks()