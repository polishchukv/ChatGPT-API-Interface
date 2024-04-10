from dotenv import load_dotenv
from openai import OpenAI
import customtkinter as ctk
import threading

load_dotenv()

class GPTGUI:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []
        self.root = ctk.Tk()
        self.root.title("GPT GUI")
        self.root.minsize(500,500)

    def setup_gui(self):
        self.root.mainloop()

app = GPTGUI()
app.setup_gui()