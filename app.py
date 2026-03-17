import customtkinter as ctk
from steam_manager import SteamManager
from server_manager import ServerProcessManager
import threading
import os
import subprocess
from tkinter import filedialog
from typing import Optional

class App(ctk.CTk):
    """Main application class for Icarus Sentinel."""

    def __init__(self) -> None:
        """Initializes the main application window and its components."""
        super().__init__()
        self.title("Icarus Sentinel")
        self.geometry("800x700")
        
        self.steam_manager = SteamManager()
        self.server_manager = ServerProcessManager()
        self.server_process: Optional[subprocess.Popen] = None
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        # Path Selection Frame
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(self.path_frame, text="Install Path:")
        self.path_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.path_entry = ctk.CTkEntry(self.path_frame)
        self.path_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.path_entry.insert(0, os.path.join(os.getcwd(), "icarus_server"))

        self.browse_button = ctk.CTkButton(
            self.path_frame, text="Browse", width=80, command=self.browse_path
        )
        self.browse_button.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Actions
        self.install_button = ctk.CTkButton(
            self, text="Install/Update Server", command=self.start_install
        )
        self.install_button.grid(row=1, column=0, padx=20, pady=10)

        # Server Control Frame
        self.mgmt_frame = ctk.CTkFrame(self)
        self.mgmt_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.start_button = ctk.CTkButton(self.mgmt_frame, text="Start Server", command=self.start_server)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = ctk.CTkButton(self.mgmt_frame, text="Stop Server", command=self.stop_server, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.restart_button = ctk.CTkButton(self.mgmt_frame, text="Restart Server", command=self.restart_server, state="disabled")
        self.restart_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.cpu_label = ctk.CTkLabel(self.mgmt_frame, text="CPU: 0.0%")
        self.cpu_label.grid(row=0, column=3, padx=10, pady=10)
        
        self.ram_label = ctk.CTkLabel(self.mgmt_frame, text="RAM: 0.00GB")
        self.ram_label.grid(row=0, column=4, padx=10, pady=10)

        self.console_output = ctk.CTkTextbox(self, state="disabled")
        self.console_output.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

    def browse_path(self) -> None:
        """Opens a directory dialog and updates the installation path entry."""
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, directory)

    def log(self, message: str) -> None:
        """Appends a message to the console output text box.

        Args:
            message: The string message to log.
        """
        self.console_output.configure(state="normal")
        self.console_output.insert("end", message + "\n")
        self.console_output.configure(state="disabled")
        self.console_output.see("end")

    def start_install(self) -> None:
        """Initiates the server installation process in a separate thread."""
        install_dir = self.path_entry.get().strip()
        if not install_dir:
            self.log("Error: Please select a valid installation directory.")
            return

        self.install_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.path_entry.configure(state="disabled")
        
        threading.Thread(
            target=self.run_install, args=(install_dir,), daemon=True
        ).start()

    def run_install(self, install_dir: str) -> None:
        """Executes the server installation and captures output for logging.

        Args:
            install_dir: The directory where the server should be installed.
        """
        self.log(f"Starting installation to: {install_dir}")
        
        try:
            process = self.steam_manager.install_server(install_dir)
            
            # Read stdout line by line
            if process.stdout:
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

    def reset_ui(self) -> None:
        """Re-enables UI elements after the installation process completes."""
        self.install_button.configure(state="normal")
        self.browse_button.configure(state="normal")
        self.path_entry.configure(state="normal")

    def start_server(self) -> None:
        """Starts the server process (Placeholder for now)."""
        pass

    def stop_server(self) -> None:
        """Stops the server process (Placeholder for now)."""
        pass

    def restart_server(self) -> None:
        """Restarts the server process (Placeholder for now)."""
        pass

def main() -> None:
    """Entry point for the application."""
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
