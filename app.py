import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, simpledialog
import os

class PromptBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LLM Prompt Builder")
        self.selected_files = []

        # Prompt input
        tk.Label(root, text="Enter your prompt:").pack(anchor="w")
        self.prompt_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=6)
        self.prompt_input.pack(fill="both", padx=10, pady=5, expand=True)

        # File list and controls
        tk.Label(root, text="Selected Code Files:").pack(anchor="w", padx=10)

        self.file_listbox = tk.Listbox(root, height=6)
        self.file_listbox.pack(fill="x", padx=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add File", command=self.add_file).pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit File", command=self.edit_file).pack(side="left", padx=5)
        tk.Button(button_frame, text="Remove File", command=self.remove_file).pack(side="left", padx=5)

        # Create a frame to hold the checkbox and directory button
        self.dir_frame = tk.Frame(root)
        self.dir_frame.pack(pady=(10, 0), anchor="center")  # This will center the checkbox and button

        # Checkbox and directory button inside the frame
        self.add_directory_var = tk.BooleanVar()
        self.add_directory_check = tk.Checkbutton(self.dir_frame, text="Add Directory", variable=self.add_directory_var, command=self.toggle_directory_button)
        self.add_directory_check.pack(pady=(0, 5))  # Padding between checkbox and button

        self.dir_button = tk.Button(self.dir_frame, text="Choose Directory", command=self.choose_directory)
        # Initially hide the button
        self.dir_button.pack_forget()

        # Generate button
        self.generate_button = tk.Button(root, text="Generate Final Prompt", command=self.generate_prompt)
        self.generate_button.pack(pady=5)

        # Output
        tk.Label(root, text="Final Prompt:").pack(anchor="w")
        self.output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15)
        self.output_box.pack(fill="both", padx=10, pady=5, expand=True)

        # Save and Copy
        out_button_frame = tk.Frame(root)
        out_button_frame.pack(pady=5)
        tk.Button(out_button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side="left", padx=5)
        tk.Button(out_button_frame, text="Save to File", command=self.save_to_file).pack(side="left", padx=5)

        self.size_label = tk.Label(root, text="Prompt size: 0 characters")
        self.size_label.pack()

    def add_file(self):
        files = filedialog.askopenfilenames(title="Select Code Files")
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.file_listbox.insert(tk.END, os.path.basename(file))
            self.generate_prompt()

    def edit_file(self):
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a file to replace.")
            return

        index = selection[0]
        new_file = filedialog.askopenfilename(title="Select Replacement File")
        if new_file:
            self.selected_files[index] = new_file
            self.file_listbox.delete(index)
            self.file_listbox.insert(index, os.path.basename(new_file))
            self.generate_prompt()

    def remove_file(self):
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a file to remove.")
            return
        index = selection[0]
        self.file_listbox.delete(index)
        del self.selected_files[index]
        self.generate_prompt()

    def toggle_directory_button(self):
        if self.add_directory_var.get():
            self.dir_button.pack(pady=(5, 10), anchor="center")  # Show the directory button below the checkbox
        else:
            self.dir_button.pack_forget()  # Hide the button

    def choose_directory(self):
        directory = filedialog.askdirectory(title="Select a Directory")
        self.chosen_directory = directory
        if not directory:
            return
        try:
            tree_str = self.build_directory_tree(directory)
            self.output_box.insert(tk.END, f"\n--- Below is the folder structure of {os.path.basename(directory)} ---\n{tree_str}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process directory: {e}")

    def build_directory_tree(self, path, indent="", is_last=True):
        tree_str = ""
        # We skip printing the root folder's name here
        basename = os.path.basename(path)
        prefix = "└── " if is_last else "├── "
        indent += "    " if is_last else "│   "  # Adjust the indentation for subfolders/files
        
        entries = sorted(os.listdir(path))
        for i, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            is_last_entry = (i == len(entries) - 1)
            if os.path.isdir(full_path):
                tree_str += f"{indent}{'└── ' if is_last_entry else '├── '}{entry}/\n"
                tree_str += self.build_directory_tree(full_path, indent, is_last_entry)
            else:
                #comment = "  # " + self.get_file_comment(full_path)
                tree_str += f"{indent}{'└── ' if is_last_entry else '├── '}{entry}\n"
        return tree_str

    def get_file_comment(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    first_line = lines[0].strip()
                    if len(first_line) > 60:
                        first_line = first_line[:57] + "..."
                    return first_line
        except:
            pass
        return "File"

    def generate_prompt(self):
        user_prompt = self.prompt_input.get("1.0", tk.END).strip()
        final = [f"{user_prompt}\n"]

        if self.add_directory_var.get():
            directory_tree = self.build_directory_tree(self.chosen_directory) if hasattr(self, 'chosen_directory') else ""
            final.append(f"\n--- Below is the folder structure of {os.path.basename(self.chosen_directory)} ---\n{directory_tree}\n" if directory_tree else "")

        for filepath in self.selected_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    contents = f.read()
                filename = os.path.basename(filepath)
                final.append(f"\n--- Below is my {filename} ---\n{contents}")
            except Exception as e:
                final.append(f"\n--- Below is my {filepath} ---\n[Error reading file: {e}]")

        combined = "\n".join(final)

        char_count = len(combined)
        warning_threshold = 400_000 

        self.size_label.config(text=f"Prompt size: {char_count:,} characters")
        if char_count > warning_threshold:
            messagebox.showwarning(
                "Prompt Size Warning",
                f"Your final prompt is approximately {char_count:,} characters long.\n\n"
                "This may exceed the input limit for some language models.\nConsider trimming your input."
            )
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, combined)

    def copy_to_clipboard(self):
        final_prompt = self.output_box.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(final_prompt)

    def save_to_file(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(self.output_box.get("1.0", tk.END))
                messagebox.showinfo("Saved", f"Prompt saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    app = PromptBuilderApp(root)
    root.mainloop()
