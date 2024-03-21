from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
import os

load_dotenv()

class GPTGUI:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []
        self.root = tk.Tk()
        self.root.title("GPT GUI")
        self.root.minsize(500,500)

    # Generate a response using the OpenAI API
    def generate_response(self):
        selected_value = self.model_version_combobox.get()
        model_version = "gpt-4" if selected_value == "4.0" else "gpt-3.5-turbo"
        prompt = self.input_field.get("1.0", tk.END).strip()
        if prompt:
            self.messages.append({"role": "user", "content": prompt})
            limited_messages = self.messages[-50:]
            completion = self.client.chat.completions.create(
                model=model_version,
                messages=limited_messages
            )
            response = completion.choices[0].message.content
            self.output_field.config(state="normal")
            self.messages.append({"role": "assistant", "content": response})
            self.output_field.insert(tk.END, f"User: {prompt}\n\n", "user")
            self.output_field.insert(tk.END, f"AI: {response}\n", "ai")
            self.output_field.insert(tk.END, "-" * 50 + "\n")
            self.input_field.delete("1.0", tk.END)
            self.loading_label.pack_forget()
            self.input_field.config(state="normal")
            self.output_field.config(state="disabled")
            self.save_button.config(state="normal")

    # Call generate_response w/ threading to prevent GUI from freezing
    def threaded_generate_response(self):
        self.input_field.config(state="disabled")
        self.loading_label.pack()
        thread = threading.Thread(target=self.generate_response)
        thread.start()

    def save_output_to_log(self, gpt_model):
        # Get the current text in the output field
        output_text = self.output_field.get("1.0", tk.END)

        # Open a dialog box for user to select log file name/path
        log_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        # Define the log file path
        log_file_path = os.path.join(os.getcwd(), 'output_log.txt')

        # Open the log file in append mode and write the output text to it
        with open(log_file_path, 'a') as log_file:
            # Record gpt_model on top of log file
            log_file.write(f"GPT Model: {gpt_model}\n")
            log_file.write("--------------------\n")

            # Write the actual output text to the log file
            log_file.write(output_text)

    def clear_history_and_input(self):
        # Delete the current text in the output field and the input field
        self.output_field.config(state="normal")
        self.output_field.delete("1.0", tk.END)
        self.input_field.delete("1.0", tk.END)
        self.output_field.config(state="disabled")

    def setup_gui(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), background="white")
        style.configure("TLabel", font=("Arial", 10))

        # Create a new frame for the input field
        input_frame = ttk.Frame(self.root, padding="10 10 10 10")
        input_frame.grid(sticky="ew")

        input_label = ttk.Label(input_frame, text="Enter your question/prompt:")
        input_label.pack()

        self.input_field = tk.Text(input_frame, height=5, width=20)
        self.input_field.pack(fill="x")

        # Create a central frame for the buttons
        button_frame = ttk.Frame(self.root, padding="10 10 10 10")
        button_frame.grid(sticky="ew")

        # Create a sub-frame for the buttons
        button_bundle_frame = ttk.Frame(button_frame)
        button_bundle_frame.pack(side="top")

        # Create the generate button
        generate_button = ttk.Button(button_bundle_frame, text="Generate Response", command=self.threaded_generate_response)
        generate_button.pack(side="left", pady=5, padx=5)

        # Create the clear button
        clear_button = ttk.Button(button_bundle_frame, text="Clear", command=self.clear_history_and_input)
        clear_button.pack(side="right", pady=5, padx=5)

        # Create a dropdown for the GPT model version
        self.model_version_combobox = ttk.Combobox(button_frame, state="readonly", width=3)
        self.model_version_combobox["values"] = ("4.0", "3.5")
        self.model_version_combobox.current(0)  # Set the default value to "4.0"
        self.model_version_combobox.pack(pady=1)
        gpt_model=self.model_version_combobox.get()

        # Create a label for the loading message, set its color to green, and hide it
        self.loading_label = ttk.Label(button_frame, text="Loading...", foreground="green")
        self.loading_label.pack_forget()

        # Create a new frame for the output field
        output_frame = ttk.Frame(self.root, padding="10 10 10 10")
        output_frame.grid(sticky="nsew")

        output_label = ttk.Label(output_frame, text="Response History:")
        output_label.pack()

        # Disable the output field by default
        self.output_field = tk.Text(output_frame, height=10, width=20, state="disabled")
        self.output_field.pack(fill="both", expand=True)

        # Add tags to the output field to color the user and AI messages
        self.output_field.tag_configure("user", foreground="black")
        self.output_field.tag_configure("ai", foreground="red")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Create a sub-frame for the log buttons
        log_button_bundle_frame = ttk.Frame(button_frame)
        log_button_bundle_frame.pack(side="bottom")

        # Create a save button to save the output to a log file by calling the save_output_to_log method
        self.save_button = ttk.Button(log_button_bundle_frame, text="Save Output", command=lambda: self.save_output_to_log(gpt_model))
        self.save_button.pack(side="left", pady=5, padx=5)
        self.save_button.config(state="disabled")

        # Create a load button to load the output from a log file and select the model version
        self.load_button = ttk.Button(log_button_bundle_frame, text="Load Output")
        self.load_button.pack(side="right", pady=5, padx=5)
        self.load_button.config(state="enabled")

        # Start the GUI
        self.root.mainloop()

app = GPTGUI()
app.setup_gui()