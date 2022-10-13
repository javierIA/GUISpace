
import threading
import time
import tkinter as tk
from turtle import update
import customtkinter 
import logging
import schedule

from runtime import execute


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Program(customtkinter.CTk):
    WIDTH = 920
    HEIGHT = 550

    def __init__(self):
        
        super().__init__()

        self.title("Space Facturas IA")
        self.geometry(f"{Program.WIDTH}x{Program.HEIGHT}")
        self.minsize(Program.WIDTH, Program.HEIGHT)
        self.maxsize(Program.WIDTH, Program.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing) 
        self.create_widgets()
        


    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=460,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self,width=460,corner_radius=0)
        self.frame_right.grid(row=0, column=1, sticky="nswe")
        self.threadisalive = False
        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  
        # empty row with minsize as spacing
        self.img= tk.PhotoImage(file="images/logo.png", master=self.frame_left)
        self.img= self.img.subsample(1,1)
        self.imageTitle = customtkinter.CTkLabel(master=self.frame_left, text="", image=self.img)
        self.imageTitle.place(relx=0.5, rely=0.18, anchor=tk.CENTER, width=300, height=160)
        self.imageTitle.grid(row=1, column=0, pady=10, padx=10)
        self.btnrun = customtkinter.CTkButton(self.frame_left, text="Run Service",
                                             text_color="#f8f8f8",command=self.runserviceThread ,width=130, height=60,hover_color="#C77C78",corner_radius=10, compound="bottom",  fg_color="#0e770c")
        self.btnrun.place(relx=0.7, rely=0.8, anchor=tk.CENTER)
        self.btnrun.grid(row=6, column=0, pady=10, padx=10)
        self.btnstop= customtkinter.CTkButton(self.frame_left, text="Stop Service", text_color="#f8f8f8",command=self.stopserverThread ,width=130, height=60,hover_color="#C77C78",corner_radius=10, compound="bottom",  fg_color="#0e770c")
        self.btnstop.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
        self.btnstop.configure(state="disabled")
        self.btnstop.grid(row=5, column=0, pady=10, padx=15)
        
        self.frame_right.grid_rowconfigure(0, minsize=10)
        self.logservice = tk.Text(master=self.frame_left, width=50, height=10,font=("Arial", 9), bg="#f8f8f8", fg="#000000", state="disabled")
        self.logservice.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=430, height=300)
        self.logservice.configure(background="#2a2d2e", foreground="white",border=0, highlightthickness=0, relief="flat")
        self.logservice.grid(row=4, column=0, pady=10, padx=10)
        
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)
        
        self.btnserver = customtkinter.CTkButton(self.frame_right, text="Run Server", text_color="#f8f8f8",command=self.ThreadServer ,width=130, height=60,hover_color="#C77C78")
        self.logserver = tk.Text(self.frame_right, width=50, height=20, state="disabled", font=("Arial", 9), bg="#f8f8f8", fg="#000000")                             
        self.logserver.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=50, height=5)
        self.logserver.configure(background="#2a2d2e", foreground="white",border=0, highlightthickness=0, relief="flat")

        self.serverThread = True
        self.btnserver.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.btnserver.grid(row=5, column=1, padx=1, pady=1)
        self.btnserverstop = customtkinter.CTkButton(self.frame_right, text="Stop Server", text_color="#f8f8f8",command=self.stopserver ,width=130, height=60,hover_color="#C77C78",state="disabled")
        self.btnserverstop.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        self.btnserverstop.grid(row=2, column=1, padx=1, pady=1)
        self.logserver.grid(row=1, column=1, padx=10, pady=10)
        # ============ frame_right ============

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
    def runServer(self):
            self.btnserver.configure(text="Running")

            executeString = execute(
            ["pwsh", "-c", "python", "server.py"],
            lambda x: self.logserver.insert(tk.END, x),
            lambda x: self.logserver.insert(tk.END,x),)
            self.logserver.insert(tk.END, executeString)
        
        
            
        
      
    def on_closing(self):
        self.destroy()
        self.quit()
    
            
if __name__ == "__main__":
   
    
    app = Program()
    app.mainloop()