import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Icarus Sentinel")
        self.geometry("800x600")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
