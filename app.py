import customtkinter as ctk
from steam_manager import SteamManager
import threading
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Icarus Sentinel")
        self.geometry("800x600")
        
        self.steam_manager = SteamManager()
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # UI Elements
        self.install_button = ctk.CTkButton(self, text="Install/Update Server", command=self.start_install)
        self.install_button.grid(row=0, column=0, padx=20, pady=20)

        self.console_output = ctk.CTkTextbox(self, state="disabled")
        self.console_output.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    def log(self, message):
        self.console_output.configure(state="normal")
        self.console_output.insert("end", message + "\n")
        self.console_output.configure(state="disabled")
        self.console_output.see("end")

    def start_install(self):
        self.install_button.configure(state="disabled")
        threading.Thread(target=self.run_install, daemon=True).start()

    def run_install(self):
        install_dir = os.path.join(os.getcwd(), "icarus_server")
        self.log(f"Starting installation to: {install_dir}")
        
        process = self.steam_manager.install_server(install_dir)
        
        for line in iter(process.stdout.readline, ""):
            if line:
                self.after(0, self.log, line.strip())
        
        process.stdout.close()
        return_code = process.wait()
        
        if return_code == 0:
            self.after(0, self.log, "Installation complete!")
        else:
            self.after(0, self.log, f"Installation failed with return code: {return_code}")
        
        self.after(0, lambda: self.install_button.configure(state="normal"))

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
