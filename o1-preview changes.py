# Update the generate_response method
def generate_response(self):
    selected_value = self.version_box.get()
    model_versions = {
        "4o": "gpt-4o",
        "4": "gpt-4-turbo",
        "3.5": "gpt-3.5-turbo",
        "o1": "o1-preview",
        "o1m": "o1-mini"
    }
    model_version = model_versions.get(selected_value)
    if not model_version:
        print(f"Invalid model version: {selected_value}.")
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
    self.output_field.insert(ctk.END, "-" * 100 + "\n")
    user_prompt_index = self.output_field.index(ctk.END)
    self.output_field.insert(ctk.END, f"AI: {response}\n", "ai")
    self.output_field.insert(ctk.END, "-" * 100 + "\n")

    self.output_field.see(user_prompt_index)

    self.input_field.delete("1.0", ctk.END)
    self.loading_label.pack_forget()
    self.input_field.configure(state="normal")
    self.output_field.configure(state="disabled")
    self.save_button.configure(state="normal")
    self.input_field.delete("1.0", ctk.END)

# Update the setup_options method to include new model options in the dropdown
def setup_options(self):
    self.options_frame = ctk.CTkFrame(self.root)
    self.options_frame.pack(fill="x", pady=10, padx=10)

    self.customize_button = ctk.CTkButton(self.options_frame, text="Customize", font=self.defaultFont, command=self.open_customization_window)
    self.customize_button.pack(side="left", padx=1)

    self.save_button = ctk.CTkButton(self.options_frame, text="Save", font=self.defaultFont, command=self.save_log)
    self.save_button.pack(side="left", padx=1)

    self.load_button = ctk.CTkButton(self.options_frame, text="Load", font=self.defaultFont, command=self.load_log)
    self.load_button.pack(side="left", padx=1)

    self.clear_button = ctk.CTkButton(self.options_frame, text="Clear", font=self.defaultFont, command=self.clear)
    self.clear_button.pack(side="left", padx=1)

    # Updated values in the dropdown menu
    self.version_box = ctk.CTkComboBox(self.options_frame,
                                       values=["4o", "4", "3.5", "o1", "o1m"],
                                       width=60, state="readonly", font=self.defaultFont)
    self.version_box.pack(side="right", padx=1)
    self.version_box.set("4o")