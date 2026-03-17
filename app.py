import customtkinter as ctk
from steam_manager import SteamManager
import threading
import os
from tkinter import filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Icarus Sentinel")
        self.geometry("800x600")
        
        self.steam_manager = SteamManager()
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        # Path Selection Frame
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(self.path_frame, text="Install Path:")
        self.path_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.path_entry = ctk.CTkEntry(self.path_frame)
        self.path_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.path_entry.insert(0, os.path.join(os.getcwd(), "icarus_server"))

        self.browse_button = ctk.CTkButton(self.path_frame, text="Browse", width=80, command=self.browse_path)
        self.browse_button.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Actions
        self.install_button = ctk.CTkButton(self, text="Install/Update Server", command=self.start_install)
        self.install_button.grid(row=1, column=0, padx=20, pady=10)

        self.console_output = ctk.CTkTextbox(self, state="disabled")
        self.console_output.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    def browse_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, directory)

    def log(self, message):
        self.console_output.configure(state="normal")
        self.console_output.insert("end", message + "\n")
        self.console_output.configure(state="disabled")
        self.console_output.see("end")

    def start_install(self):
        install_dir = self.path_entry.get().strip()
        if not install_dir:
            self.log("Error: Please select a valid installation directory.")
            return

        self.install_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.path_entry.configure(state="disabled")
        
        threading.Thread(target=self.run_install, args=(install_dir,), daemon=True).start()

    def run_install(self, install_dir):
        self.log(f"Starting installation to: {install_dir}")
        
        try:
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
        except Exception as e:
            self.after(0, self.log, f"An error occurred: {str(e)}")
        
        self.after(0, self.reset_ui)

    def reset_ui(self):
        self.install_button.configure(state="normal")
        self.browse_button.configure(state="normal")
        self.path_entry.configure(state="normal")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
