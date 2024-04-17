from dotenv import load_dotenv
from openai import OpenAI
import customtkinter as ctk
import threading

load_dotenv()

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class customGPTGUI:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []
        self.root = ctk.CTk()
        self.root.title("GPT GUI v2")
        self.root.minsize(500,500)

    def setupInput(self):
        # Create a new frame for the input field
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(fill="x", pady=10, padx=10)  # Add fill and expand options

        ctk.CTkLabel(self.input_frame, text="", height=1).pack()

        self.input_field = ctk.CTkTextbox(self.input_frame)
        self.input_field.pack(fill="x", expand=True, padx=10)

        self.input_button = ctk.CTkButton(self.input_frame, text="Generate Response", width=20, command=self.testCommand)
        self.input_button.pack(pady=10)
        self.input_field.bind("<Shift-Return>", self.shiftEnter)

    def shiftEnter(self, event):
        self.input_button.invoke()
        return "break"

    def setupOptions(self):
        self.options_frame = ctk.CTkFrame(self.root)
        self.options_frame.pack(fill="x", pady=10, padx=10)

        self.save_button = ctk.CTkButton(self.options_frame, text="Save Output", width=10)
        self.save_button.pack(side="left", padx=1)

        self.load_button = ctk.CTkButton(self.options_frame, text="Load Output", width=10)
        self.load_button.pack(side="left", padx=1)

        self.load_button = ctk.CTkButton(self.options_frame, text="Clear", width=10)
        self.load_button.pack(side="left", padx=1)

        self.version_box = ctk.CTkComboBox(self.options_frame, values=["4.0", "3.5"], command=self.testCommand, width=60, state="readonly")
        self.version_box.pack(side="right", padx=1)
        self.version_box.set("4.0")

    def setupOutput(self):
        # Create a new frame for the output field
        self.output_frame = ctk.CTkFrame(self.root)
        self.output_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # Create an output field
        self.output_field = ctk.CTkTextbox(self.output_frame, state="disabled")
        self.output_field.pack(padx=10, pady=10, fill="both", expand=True)

    def testCommand(self):
        print(self.version_box.get())

    def setupGUI(self):
        self.setupOptions()
        self.setupInput()
        self.setupOutput()
        self.root.mainloop()

app = customGPTGUI()
app.setupGUI()