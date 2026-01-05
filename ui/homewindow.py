import customtkinter as ctk
import datetime
from ui.controller import Controller

class HomeWindow(ctk.CTkFrame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller: Controller = controller
        self.current_record = None # Cache the record for the timer
        self.timer_running = False

        # --- Grid Configuration ---
        # 3 Columns of equal width (uniform="a" forces them to match)
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        
        # 2 Rows: Row 0 takes all extra space, Row 1 is for buttons
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=0)

        # ================= UPPER SECTION (Stats) =================
        
        # --- LEFT: Remaining Days ---
        self.frame_left = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=2, pady=5)
        
        self.lbl_days_val = ctk.CTkLabel(self.frame_left, text="--", font=("Arial", 28, "bold"), text_color="#3B8ED0")
        self.lbl_days_val.pack(expand=True, anchor="s") 
        self.lbl_days_title = ctk.CTkLabel(self.frame_left, text="Days Left", font=("Arial", 12), text_color="gray")
        self.lbl_days_title.pack(expand=True, anchor="n") 

        # --- MIDDLE: Data Usage ---
        self.frame_mid = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_mid.grid(row=0, column=1, sticky="nsew", padx=2, pady=5)

        # Create an inner container that stays perfectly centered
        self.mid_inner = ctk.CTkFrame(self.frame_mid, fg_color="transparent")
        self.mid_inner.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Big Number (Remaining) - Row 0, Column 0
        self.lbl_remain_val = ctk.CTkLabel(
            self.mid_inner, 
            text="--",  # Placeholder
            font=("Arial", 25, "bold"), 
            text_color="#FFAEFF"
        )
        self.lbl_remain_val.grid(row=0, column=0, sticky="e", padx=(0, 5))

        # 2. "Remaining" Text - Row 0, Column 1
        self.lbl_remain_text = ctk.CTkLabel(
            self.mid_inner, 
            text="rem", 
            font=("Arial", 10), 
            text_color="#FFAEFF"
        )
        # self.lbl_remain_text.grid(row=0, column=1, sticky="w")

        # 3. Small Number (Used) - Row 1, Spans both columns
        self.lbl_used = ctk.CTkLabel(
            self.mid_inner, 
            text="-- Used", # Placeholder
            font=("Arial", 12), 
            text_color="#888888"
        )
        self.lbl_used.grid(row=1, column=0, columnspan=2)

        # --- RIGHT: Active Seconds ---
        self.frame_right = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_right.grid(row=0, column=2, sticky="nsew", padx=2, pady=5)
        
        self.lbl_active_val = ctk.CTkLabel(self.frame_right, text="--", font=("Arial", 28, "bold"))
        self.lbl_active_val.pack(expand=True, anchor="s")
        self.lbl_active_title = ctk.CTkLabel(self.frame_right, text="Sec Active", font=("Arial", 12), text_color="gray")
        self.lbl_active_title.pack(expand=True, anchor="n")

        # ================= LOWER SECTION (Buttons) =================
        
        self.frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_btns.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=10)
        self.frame_btns.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_refresh = ctk.CTkButton(self.frame_btns, text="Refresh", command=self.manual_refresh, 
                                         fg_color="#3B8ED0", height=35)
        self.btn_refresh.grid(row=0, column=0, sticky="ew", padx=5)

        self.btn_dismiss = ctk.CTkButton(self.frame_btns, text="Dismiss", command=self.dismiss_action, 
                                         fg_color="gray", height=35)
        self.btn_dismiss.grid(row=0, column=1, sticky="ew", padx=5)

        self.btn_logout = ctk.CTkButton(self.frame_btns, text="Logout", command=self.logout_action, 
                                        fg_color="#D03B3B", height=35)
        self.btn_logout.grid(row=0, column=2, sticky="ew", padx=5)

        # Start logic
        self.manual_refresh()
        self.start_timer()

    def manual_refresh(self):
        """Fetches fresh data from controller."""
        # 1. Change UI to loading state
        self.btn_refresh.configure(text="Loading...", state="disabled", cursor="wait")
        
        # 2. FORCE the UI to redraw immediately!
        self.update_idletasks() 
        
        # 3. Perform the heavy operation (App will freeze here)
        try:
            self.current_record = self.controller.get_record()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # 4. Restore UI state (This runs even if there is an error)
            self.btn_refresh.configure(text="Refresh", state="normal", cursor="arrow")
            self.update_static_ui()

    def update_static_ui(self):
        """Updates elements that don't change every second."""
        if self.current_record:
            # 1. Update Days Left
            try:
                expire_date = datetime.datetime.fromtimestamp(self.current_record.expireTime / 1000)
                now = datetime.datetime.now()
                delta = expire_date - now
                days = delta.days if delta.days >= 0 else 0
                self.lbl_days_val.configure(text=str(days))
            except Exception:
                self.lbl_days_val.configure(text="--")

            # 2. Update Middle Section (Usage Data)
            try:
                remain = self.current_record.remain 
                used = self.current_record.used              
                self.lbl_remain_val.configure(text=f"{remain:.2f}")
                self.lbl_used.configure(text=f"{used:.2f} Used")
            except Exception:
                self.lbl_remain_val.configure(text="Err")
                self.lbl_used.configure(text="-- Used")

        else:
            self.lbl_days_val.configure(text="Err")
            self.lbl_remain_val.configure(text="Err")

    def start_timer(self):
        self.update_active_seconds()
        self.after(1000, self.start_timer)

    def update_active_seconds(self):
        if self.current_record:
            val = self.current_record.get_secounds_left() 
            self.lbl_active_val.configure(text=str(val))
        else:
             self.lbl_active_val.configure(text="--")

    def dismiss_action(self):
        self.controller.dismiss_callback()

    def logout_action(self):
        self.controller.logout()