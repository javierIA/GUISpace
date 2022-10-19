import threading
import time
import tkinter as tk
import customtkinter 
import logging
import schedule
import pystray
from runtime import execute
from pystray import Menu, MenuItem as item
from PIL import Image
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Program(customtkinter.CTk):
    WIDTH = 680
    HEIGHT = 750

    def __init__(self):
        
        super().__init__()

        self.title("Space Facturas IA")
        self.geometry(f"{Program.WIDTH}x{Program.HEIGHT}")
        self.minsize(Program.WIDTH, Program.HEIGHT)
        self.maxsize(Program.WIDTH, Program.HEIGHT)
        self.create_widgets()
        self.withdraw_window()
        


    def create_widgets(self):

        
        # empty row with minsize as spacing
        self.img= tk.PhotoImage(file="images/logo.png", master=self)
        self.img= self.img.subsample(1,1)
        self.imageTitle = customtkinter.CTkLabel(master=self, text="", image=self.img)
        self.imageTitle.place(relx=0.7, rely=0.18, anchor=tk.CENTER, width=300, height=200)
        self.imageTitle.grid(row=1, column=0, pady=10, padx=0)
        self.btnrun = customtkinter.CTkButton(self, text="Run Service",
                                             text_color="#f8f8f8",command=self.runserviceThread ,width=130, height=60,hover_color="#C77C78",corner_radius=10, compound="bottom",  fg_color="#0e770c")
        self.btnrun.place(relx=0.7, rely=0.8, anchor=tk.CENTER)
        self.btnrun.grid(row=6, column=0, pady=10, padx=0)
        self.btnstop= customtkinter.CTkButton(self, text="Stop Service", text_color="#f8f8f8",command=self.stopserverThread ,width=130, height=60,hover_color="#C77C78",corner_radius=10, compound="bottom",  fg_color="#0e770c")
        self.btnstop.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
        self.btnstop.configure(state="disabled")
        self.btnstop.grid(row=5, column=0, pady=0, padx=0)
        
        self.logservice = tk.Text(master=self, width=100, height=25,font=("Arial", 9), bg="#f8f8f8", fg="#000000", state="disabled")
        self.logservice.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=680, height=450)
        self.logservice.configure(background="#2a2d2e", foreground="white",border=0, highlightthickness=0, relief="flat")
        self.logservice.grid(row=4, column=0, pady=10, padx=0)
     
    def withdraw_window(self):  
        image = Image.open("images/logo.png")
        menu = (item('Quit', self.on_closing), item('Show', self.show_win),item('Hide', self.hide_win))
        icon = pystray.Icon("name", image, "title", menu)
        icon.run()
    

    def updateText(self, text):
        self.logservice.insert(tk.END, text)
        self.logservice.see(tk.END)
    def runservice(self):
        self.btnrun.configure(state="disabled", text="Running")
        self.btnstop.configure(state="normal")
        self.logservice.configure(state="normal")
        executeString = execute(
            ["pwsh", "-c", "python", "service.py"],
            lambda x: self.logservice.insert(tk.END, x),
            lambda x: self.updateText(x),)
            
        self.logservice.insert(tk.END, executeString)   
        self.logservice.configure(state="disabled")
    
    def ThreadServer(self):
        if self.serverThread:
            self.serverThread = False
            self.btnserver.configure(state="disabled")
            self.btnserverstop.configure(state="normal")
            self.logserver.configure(state="normal")
            self.logserver.insert(tk.END, "Server is running")
            self.logserver.see(tk.END)
            self.logserver.configure(state="normal")
            self.server = threading.Thread(target=self.runServer)
            self.server.start()
        
    
    
    def runserviceThread(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logservice.insert(tk.END, "Starting server ... "+".\n")
        logging.debug('Start of program.')
        self.btnrun.configure(state="disabled", text="Running")
        self.btnstop.configure(state="normal")
        schedule.every(100).seconds.do(self.runservice)
        self.threadisalive = True
        self.thread = threading.Thread(target=self.thread_control)
        self.thread.start()
        
    def stopserverThread(self):
        self.btnrun.configure(state="normal", text="Run Service")
        self.btnstop.configure(state="disabled")
        self.logservice.configure(state="normal")
        self.threadisalive = False
    def stopserver(self):
        self.logserver.insert(tk.END, "Server is stopped")
        self.btnserverstop.configure(state="disabled")
        self.btnserver.configure(state="normal")
        self.serverThread = False
        self.logserver.configure(state="disabled")
        self.btnserverstop.configure(state="disabled")
        self.serverThread = True
        
    def thread_control(self):
        if self.threadisalive:
            while 1:
                schedule.run_pending()
                time.sleep(1)
      
    def on_closing(self,icon):
        self.destroy()
        icon.stop();
        self.quit()
        
    def show_win(self,icon):
        icon.stop()
        self.after(0,self.deiconify)
    def hide_win(self  ):

        self.iconify()
            
if __name__ == "__main__":
    
    app = Program()
    app.protocol('WM_DELETE_WINDOW', app.withdraw_window)
    app.mainloop()

    
        