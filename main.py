import customtkinter as ctk
from ui import MainView

def main():
    # Create the main window (CTk)
    window = ctk.CTk()
    window.title("Custom Tkinter App")
    window.geometry("400x300")

    # Create an instance of the App frame inside the main window
    MainView(master=window)
    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
