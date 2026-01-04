import core 
import customtkinter as ctk
from typing import Any, Callable
class Controller:
    def __init__(self , view : ctk.CTkFrame, dismiss_callback : Callable[[], Any]=None):
        self.user = core.User()
        self.view = view
        self.current_window = None 
        self.dismiss_callback = dismiss_callback
        if not self.user.isAuth:
            self.show_login()
        else:
            self.show_main()

    def show_login(self):
        if self.current_window:
            self.current_window.pack_forget()
        from ui.loginwindow import loginWindow
        self.current_window = loginWindow(self.view, self)
        self.current_window.pack(expand=True, fill="both")
        self.view.update()

    def show_main(self):
        if self.current_window:
            self.current_window.pack_forget()
        from ui.homewindow   import HomeWindow
        self.current_window = HomeWindow(self.view , self)
        self.current_window.pack(expand=True, fill="both")
        self.view.update()
   
    def login(self, username, password) -> bool:
        test = core.User(load=False,username=username, password=password)
        test.getToken()
        if test.is_logged_in == False:
            return False
        else:
            self.user = test
            self.show_main()
            return True
    
    def logout(self):
        self.user.clear()
        self.user = core.User()
        self.show_login()
    
    def get_record(self):
        return self.user.getRecord()
  