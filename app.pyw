import tkinter as tk
import pystray
from PIL import Image, ImageDraw
import threading
import sys
from ui import *

class NotificationTrayApp:
    def __init__(self):
        # 1. Setup the specific "Notification Style" Window
        self.root = tk.Tk()
        self.root.title("Tray Notification")
        
        # Remove window border/title bar (Frameless)
        self.root.overrideredirect(True)
        
        # Keep window on top of others
        self.root.wm_attributes("-topmost", True)
        
        # styling variables
        self.width = 300
        self.height = 150
        bg_color = "#333333"  # Dark gray background
        text_color = "#FFFFFF"
        
        self.root.configure(bg=bg_color)

        # 2. Add Content to the "Notification"

        MainView(master=self.root , dismiss_callback=self.hide_window)
        # Close button inside the popup


        # 3. Auto-hide when user clicks away (loses focus)
        self.root.bind("<FocusOut>", lambda e: self.hide_window())

        # 4. Setup Tray Icon
        self.tray_icon = None
        self.start_tray_icon()

        # 5. Start Hidden
        self.hide_window()
        self.root.mainloop()

    def create_image(self):
        # Create a simple Red/White icon
        w, h = 64, 64
        image = Image.new('RGB', (w, h), "#D32F2F") # Red
        dc = ImageDraw.Draw(image)
        dc.ellipse((16, 16, 48, 48), fill="white")
        return image

    def calculate_position(self):
        """Calculates X/Y coordinates to put window at bottom-right of screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Adjust these offsets if it overlaps your taskbar too much
        x_offset = 20
        y_offset = 50 

        x = screen_width - self.width - x_offset
        y = screen_height - self.height - y_offset
        
        return f"{self.width}x{self.height}+{x}+{y}"

    def start_tray_icon(self):
        menu = pystray.Menu(
            pystray.MenuItem("Show Notification", self.show_window, default=True),
            pystray.MenuItem("Exit", self.quit_app)
        )
        
        image = self.create_image()
        self.tray_icon = pystray.Icon("name", image, "My Notifier", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon=None, item=None):
        # Calculate position every time (in case user changed resolution)
        geom = self.calculate_position()
        
        self.root.after(0, lambda: self.root.geometry(geom))
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.root.lift) # Bring to front
        self.root.after(0, self.root.focus_force()) # Grab focus so <FocusOut> works

    def hide_window(self):
        self.root.withdraw()

    def quit_app(self, icon, item):
        self.tray_icon.stop()
        self.root.after(0, self.root.quit)
        sys.exit()

if __name__ == "__main__":
    app = NotificationTrayApp()