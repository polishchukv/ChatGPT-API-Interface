from dotenv import load_dotenv
from openai import OpenAI
import customtkinter as ctk
import threading

#load_dotenv()

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class customGPTGUI:
    def __init__(self):
        #self.client = OpenAI()
        self.messages = []
        self.root = ctk.CTk()
        self.root.title("GPT GUI v2")
        self.root.minsize(500,500)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = int((screen_width/2) - (500/2))
        y_coordinate = int((screen_height/2) - (500/2))

        self.root.geometry(f"+{x_coordinate}+{y_coordinate}")

        self.defaultFont=ctk.CTkFont(family="Roboto", size=15)

    def setupInput(self):
        # Create a new frame for the input field
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(fill="x", pady=10, padx=10)  # Add fill and expand options

        ctk.CTkLabel(self.input_frame, text="", height=1).pack()

        self.input_field = ctk.CTkTextbox(self.input_frame, font=self.defaultFont)
        self.input_field.pack(fill="x", expand=True, padx=10)

        self.input_button = ctk.CTkButton(self.input_frame, text="Generate Response", font=self.defaultFont, width=20, command=self.testCommand)
        self.input_button.pack(pady=10)
        self.input_field.bind("<Shift-Return>", self.shiftEnter)

    def shiftEnter(self, event):
        self.input_button.invoke()
        return "break"

    def setupOptions(self):
        self.options_frame = ctk.CTkFrame(self.root)
        self.options_frame.pack(fill="x", pady=10, padx=10)

        self.customize_button = ctk.CTkButton(self.options_frame, text="Customize", width=10, font=self.defaultFont, command=self.open_customization_window)
        self.customize_button.pack(side="left", padx=1)

        self.save_button = ctk.CTkButton(self.options_frame, text="Save", width=10, font=self.defaultFont)
        self.save_button.pack(side="left", padx=1)

        self.load_button = ctk.CTkButton(self.options_frame, text="Load", width=10, font=self.defaultFont, command=self.load_log)
        self.load_button.pack(side="left", padx=1)

        self.clear_button = ctk.CTkButton(self.options_frame, text="Clear", width=10, font=self.defaultFont)
        self.clear_button.pack(side="left", padx=1)

        self.version_box = ctk.CTkComboBox(self.options_frame, values=["4.0", "3.5"], width=60, state="readonly", font=self.defaultFont, command=self.testCommand)
        self.version_box.pack(side="right", padx=1)
        self.version_box.set("4.0")

    def load_log(self):
        # Open a dialog box for user to select log file name/path
        log_file_path = ctk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    def open_customization_window(self):
        try: 
            self.customization_window.lift()
        except: 
            self.customization_window = ctk.CTkToplevel(self.root)
            self.customization_window.title("Customization")
            self.customization_window.attributes("-topmost", True)
            self.customization_window.minsize(500, 500)

            # Get the screen width and height
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # Calculate the position to center the window
            x_coordinate = (screen_width // 2) - (self.customization_window.winfo_width() // 2)
            y_coordinate = (screen_height // 2) - (self.customization_window.winfo_height() // 2)

            # Set the position of the window
            self.customization_window.geometry(f"+{x_coordinate}+{y_coordinate}")

    def setupOutput(self):
        # Create a new frame for the output field
        self.output_frame = ctk.CTkFrame(self.root)
        self.output_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # Create an output field
        self.output_field = ctk.CTkTextbox(self.output_frame, state="disabled", font=self.defaultFont)
        self.output_field.pack(padx=10, pady=10, fill="both", expand=True)

    def testCommand(self):
        #print(self.version_box.get())
        
        user_input = self.input_field.get("1.0", "end-1c")
        self.output_field.configure(state="normal")
        self.output_field.insert("end", "User: " + "\n" + user_input + "\n\n")
        self.output_field.configure(state="disabled")

    def setupGUI(self):
        self.setupOptions()
        self.setupInput()
        self.setupOutput()
        self.root.mainloop()

app = customGPTGUI()
app.setupGUI()