import customtkinter as ctk
from steam_manager import SteamManager
from server_manager import ServerProcessManager
import threading
import os
import subprocess
import psutil
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

        # Recover state
        self.recover_state()

        # Start monitoring loop
        self.update_monitoring()

    def recover_state(self) -> None:
        """Attempts to recover the server process from saved state."""
        saved_pid = self.server_manager.state.get("pid")
        if saved_pid:
            try:
                p = psutil.Process(saved_pid)
                if p.is_running():
                    self.log(f"Recovered existing server process (PID: {saved_pid})")
                    self.server_process = saved_pid
                    self.start_button.configure(state="disabled")
                    self.stop_button.configure(state="normal")
                    self.restart_button.configure(state="normal")
                else:
                    self.reset_state()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.reset_state()

    def reset_state(self) -> None:
        """Resets the server state in the manager."""
        self.server_manager.state["pid"] = None
        self.server_manager.state["status"] = "stopped"
        self.server_manager.save_state()

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

    def get_server_executable(self, install_dir: str) -> Optional[str]:
        """Resolves the path to the actual server executable.

        Args:
            install_dir: The base installation directory.

        Returns:
            The full path to the executable, or None if not found.
        """
        # Common relative path for Icarus Dedicated Server
        shipping_exe = os.path.join(
            install_dir, "Icarus", "Binaries", "Win64", "IcarusServer-Win64-Shipping.exe"
        )
        if os.path.exists(shipping_exe):
            return shipping_exe
        
        # Fallback to root exe if present (though usually just a launcher)
        root_exe = os.path.join(install_dir, "IcarusServer.exe")
        if os.path.exists(root_exe):
            return root_exe
            
        return None

    def start_server(self) -> None:
        """Starts the server process in a separate thread."""
        install_dir = self.path_entry.get().strip()
        if not install_dir or not os.path.exists(install_dir):
            self.log("Error: Invalid installation directory.")
            return

        exe_path = self.get_server_executable(install_dir)
        if not exe_path:
            self.log("Error: Could not find IcarusServer executable in the selected directory.")
            return

        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.restart_button.configure(state="normal")
        
        threading.Thread(
            target=self.run_server, args=(exe_path,), daemon=True
        ).start()

    def run_server(self, exe_path: str) -> None:
        """Starts the server and streams logs."""
        try:
            self.server_process = self.server_manager.start_server(exe_path)
            self.log(f"Server started (PID: {self.server_process.pid})")
            
            # Start log streaming (blocks until process exit)
            self.server_manager.stream_logs(self.server_process, lambda line: self.after(0, self.log, line))
            
            # If stream_logs returns, the process has exited
            self.after(0, self.on_server_exit)
        except Exception as e:
            self.after(0, self.log, f"Server error: {str(e)}")
            self.after(0, self.on_server_exit)

    def on_server_exit(self) -> None:
        """Handles server process exit UI updates."""
        if self.server_process is None:
            return

        self.log("Server process has exited.")
        self.server_process = None
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.restart_button.configure(state="disabled")
        self.cpu_label.configure(text="CPU: 0.0%")
        self.ram_label.configure(text="RAM: 0.00GB")

    def stop_server(self) -> None:
        """Stops the server process."""
        if self.server_process:
            self.log("Stopping server...")
            self.server_manager.stop_server(self.server_process)
            
            # If it's a PID (recovered process), the log reader thread isn't running,
            # so we manually trigger the exit UI cleanup.
            if isinstance(self.server_process, int):
                self.on_server_exit()
            self.log("Server stop signal sent successfully.")

    def restart_server(self) -> None:
        """Restarts the server process."""
        exe_path = self.path_entry.get().strip()
        if self.server_process and exe_path:
            self.log("Restarting server...")
            self.server_manager.stop_server(self.server_process)
            # start_server will be called by the thread or manually
            self.start_server()

    def update_monitoring(self) -> None:
        """Updates the resource usage labels every 5 seconds."""
        if self.server_process:
            usage = self.server_manager.get_resource_usage(self.server_process)
            self.after(0, lambda: self.cpu_label.configure(text=f"CPU: {usage['cpu']}%"))
            self.after(0, lambda: self.ram_label.configure(text=f"RAM: {usage['ram_gb']}GB"))
            
        self.after(5000, self.update_monitoring)

def main() -> None:
    """Entry point for the application."""
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
