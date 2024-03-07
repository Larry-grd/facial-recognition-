import tkinter as tk
import registration
from start_page import LoginScreen
from homePage import HomePage

class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(LoginScreen)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(fill="both", expand=True)

    def show_start_page(self):
        self.switch_frame(LoginScreen)

if __name__ == "__main__": 
    app = MainApplication()
    app.mainloop()