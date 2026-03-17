import json
import os

class ServerProcessManager:
    def __init__(self, state_file="server_state.json"):
        self.state_file = state_file
        self.state = {"pid": None, "status": "stopped"}
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    self.state = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.state = {"pid": None, "status": "stopped"}

    def save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f)
        except IOError:
            pass
