from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import ttk
import threading

load_dotenv()


class GPTGUI:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []
        self.root = tk.Tk()
        self.root.title("GPT GUI")
        self.root.minsize(500,500)

    def generate_response(self):
        selected_value = self.model_version_combobox.get()
        model_version = "gpt-4" if selected_value == "4.0" else "gpt-3.5-turbo"
        prompt = self.input_field.get("1.0", tk.END).strip()
        if prompt:
            self.messages.append({"role": "user", "content": prompt})
            limited_messages = self.messages[-20:]
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

    def threaded_generate_response(self):
        self.input_field.config(state="disabled")
        self.loading_label.pack()
        thread = threading.Thread(target=self.generate_response)
        thread.start()

    def setup_gui(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), background="white")
        style.configure("TLabel", font=("Arial", 10))

        input_frame = ttk.Frame(self.root, padding="10 10 10 10")
        input_frame.grid(sticky="ew")

        input_label = ttk.Label(input_frame, text="Enter your question/prompt:")
        input_label.pack()

        self.input_field = tk.Text(input_frame, height=5, width=20)
        self.input_field.pack(fill="x")

        button_frame = ttk.Frame(self.root, padding="10 10 10 10")
        button_frame.grid(sticky="ew")

        generate_button = ttk.Button(button_frame, text="Generate Response", command=self.threaded_generate_response)
        generate_button.pack(pady=3)

        self.model_version_combobox = ttk.Combobox(button_frame, state="readonly", width=3)
        self.model_version_combobox["values"] = ("4.0", "3.5")
        self.model_version_combobox.current(0)  # Set the default value to "4.0"
        self.model_version_combobox.pack(pady=1)

        self.loading_label = ttk.Label(button_frame, text="Loading...", foreground="green")
        self.loading_label.pack_forget()

        output_frame = ttk.Frame(self.root, padding="10 10 10 10")
        output_frame.grid(sticky="nsew")

        output_label = ttk.Label(output_frame, text="Response History:")
        output_label.pack()

        self.output_field = tk.Text(output_frame, height=10, width=20, state="disabled")
        self.output_field.pack(fill="both", expand=True)

        self.output_field.tag_configure("user", foreground="blue")
        self.output_field.tag_configure("ai", foreground="red")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.root.mainloop()

app = GPTGUI()
app.setup_gui()