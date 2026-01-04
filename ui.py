import customtkinter as ctk
import model  # Assuming model.py contains the User class

class App(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)  # Initialize the CTkFrame parent class
        self.pack(padx=20, pady=20, expand=True, fill="both")

        # Create an instance of the User model
        user = model.User()

        # Depending on the authentication status, show either home or login
        if user.isAuth:
            self.show_home_window()
        else:
            self.show_login_window()

    def show_home_window(self):
        # Create the home window and pack it into the App frame
        home = mainWindow(self)
        home.pack(expand=True, fill="both")

    def show_login_window(self):
        # Create the login window and pack it into the App frame
        login = loginWindow(self)
        login.pack(expand=True, fill="both")

class loginWindow(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="Login Screen")
        self.label.pack(pady=10)

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
        print("Login attempted")

class mainWindow(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="Home Screen")
        self.label.pack(pady=10)

        # Add home page widgets here
        # Example: Logout button
        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout_action)
        self.logout_button.pack(pady=10)

    def logout_action(self):
        # Add your logout logic here
        print("Logout initiated")
        # Optionally, you could switch back to the login window by re-instantiating App or refreshing
        self.master.destroy()

def main():
    # Create the main window (CTk)
    window = ctk.CTk()
    window.title("Custom Tkinter App")
    window.geometry("400x300")

    # Create an instance of the App frame inside the main window
    app_frame = App(master=window)

    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
