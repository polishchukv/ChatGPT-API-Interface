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

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = int((screen_width/2) - (500/2))
        y_coordinate = int((screen_height/2) - (500/2))

        self.root.geometry(f"+{x_coordinate}+{y_coordinate}")

        self.defaultFont=ctk.CTkFont(family="Roboto", size=15)

    # Generate a response using the OpenAI API
    def generate_response(self):
        selected_value = self.version_box.get()
        if selected_value == "4o":
            model_version = "gpt-4o"
        elif selected_value == "4":
            model_version = "gpt-4-turbo"
        elif selected_value == "3.5":
            model_version = "gpt-3.5-turbo"
        prompt = self.input_field.get("1.0", ctk.END).strip()
        if not prompt:  # Check if prompt is empty
            return  # Do nothing
        self.input_field.configure(state="disabled")
        self.loading_label.pack(side="left", padx=10)
        self.messages.append({"role": "user", "content": prompt})
        limited_messages = self.messages[-100:]
        completion = self.client.chat.completions.create(
            model=model_version,
            messages=limited_messages
        )
        response = completion.choices[0].message.content
        self.output_field.configure(state="normal")
        self.messages.append({"role": "assistant", "content": response})
        self.output_field.insert(ctk.END, f"User: {prompt}\n\n", "user")
        self.output_field.insert(ctk.END, f"AI: {response}\n", "ai")
        self.output_field.insert(ctk.END, "-" * 50 + "\n")
        self.input_field.delete("1.0", ctk.END)
        self.loading_label.pack_forget()
        self.input_field.configure(state="normal")
        self.output_field.configure(state="disabled")
        self.save_button.configure(state="normal")
        self.input_field.delete("1.0", ctk.END)

    # Call generate_response w/ threading to prevent GUI from freezing
    def threaded_generate_response(self):
        thread = threading.Thread(target=self.generate_response)
        thread.start()

    def load_log(self):
        # Open a dialog box for user to select log file name/path
        log_file_path = ctk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if log_file_path:  # Check if a file was selected
            with open(log_file_path, 'r') as log_file:
                # Parse beginning of log file to get the GPT model version
                first_line = log_file.readline()
                model_version = first_line.split("GPT Model: ")[1].strip()

                # Select the combobox option based on the model_version
                if model_version == "4o":
                    self.version_box.current(0)  # Set the combobox value to "4.0"
                elif model_version == "4":
                    self.version_box.current(1)  # Set the combobox value to "3.5"
                elif model_version == "3.5":
                    self.version_box.current(2)  # Set the combobox value to "4o"
                else:
                    print(f"Invalid model version: {model_version}")

                # Skip the next line
                log_file.readline()

                # Load conversation history
                loaded_messages = []
                for line in log_file:
                    if line.startswith("User: "):
                        loaded_messages.append({"role": "user", "content": line[6:].strip()})
                    elif line.startswith("AI: "):
                        loaded_messages.append({"role": "assistant", "content": line[4:].strip()})
                    elif line.startswith(" "):
                        pass

                # Clear the existing messages and append the loaded messages
                self.messages = loaded_messages

                # Clear the output field and append the loaded conversation
                self.output_field.configure(state="normal")
                self.output_field.delete("1.0", ctk.END)
                for message in loaded_messages:
                    content = message["content"]
                    if message["role"] == "user":
                        self.output_field.insert(ctk.END, f"User: {content}\n\n", "user")
                    elif message["role"] == "assistant":
                        self.output_field.insert(ctk.END, f"AI: {content}\n", "ai")
                self.output_field.insert(ctk.END, "-" * 50 + "\n")
                self.output_field.configure(state="disabled")

                self.generate_response()
            '''
            # Read the log file and insert the content into the output field
            log_content = log_file.read()
            self.output_field.configure(state="normal")
            self.output_field.insert(tk.END, "\nIMPORTED CONVERSATION:\n" + log_content)
            self.output_field.configure(state="disabled")
            '''

    def save_log(self):
        # Get the selected GPT model version
        gpt_model = self.version_box.get()

        # Get the current text in the output field
        output_text = self.output_field.get("1.0", ctk.END)

        # Open a dialog box for user to select log file name/path
        log_file_path = ctk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        # Open the log file in append mode and write the output text to it
        with open(log_file_path, 'a') as log_file:
            # Record gpt_model on top of log file
            log_file.write(f"GPT Model: {gpt_model}\n")
            log_file.write("--------------------\n")

            # Write the actual output text to the log file
            log_file.write(output_text)

    def clear(self):
        # Delete the current text in the output field and the input field
        self.output_field.configure(state="normal")
        self.output_field.delete("1.0", ctk.END)
        self.input_field.delete("1.0", ctk.END)
        self.output_field.configure(state="disabled")

    def setupInput(self):
        # Create a new frame for the input field
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(fill="x", pady=10, padx=10)  # Add fill and expand options

        ctk.CTkLabel(self.input_frame, text="", height=1).pack()

        self.input_field = ctk.CTkTextbox(self.input_frame, font=self.defaultFont)
        self.input_field.pack(fill="x", expand=True, padx=10)

        self.input_button = ctk.CTkButton(self.input_frame, text="Generate Response", font=self.defaultFont, width=20, command=self.threaded_generate_response)
        self.input_button.pack(side="right", pady=10, padx=10)
        self.input_field.bind("<Shift-Return>", self.shiftEnter)

        # Create a label for the loading message, set its color to green, and hide it
        self.loading_label = ctk.CTkLabel(self.input_frame, text="Loading...", fg_color="green")
        self.loading_label.pack_forget()

    def shiftEnter(self, event):
        self.input_button.invoke()
        return "break"

    def setupOptions(self):
        self.options_frame = ctk.CTkFrame(self.root)
        self.options_frame.pack(fill="x", pady=10, padx=10)

        self.customize_button = ctk.CTkButton(self.options_frame, text="Customize", width=10, font=self.defaultFont, command=self.open_customization_window)
        self.customize_button.pack(side="left", padx=1)

        self.save_button = ctk.CTkButton(self.options_frame, text="Save", width=10, font=self.defaultFont, command=self.save_log)
        self.save_button.pack(side="left", padx=1)

        self.load_button = ctk.CTkButton(self.options_frame, text="Load", width=10, font=self.defaultFont, command=self.load_log)
        self.load_button.pack(side="left", padx=1)

        self.clear_button = ctk.CTkButton(self.options_frame, text="Clear", width=10, font=self.defaultFont, command=self.clear)
        self.clear_button.pack(side="left", padx=1)

        self.version_box = ctk.CTkComboBox(self.options_frame, values=["4o", "4", "3.5"], width=60, state="readonly", font=self.defaultFont)
        self.version_box.pack(side="right", padx=1)
        self.version_box.set("4o")

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