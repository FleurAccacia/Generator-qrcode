import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from qrCode import generer_qr_code_avec_logo_et_degrade, generer_qr_code_avec_logo, creer_degraded_qr, generer_qr_code_personnalise, generer_qr_code
from PIL import Image, ImageTk
import os

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")

        # Main frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack()

        # --- Options Frame ---
        options_frame = tk.LabelFrame(main_frame, text="Options")
        options_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        # Data
        self.data_label = tk.Label(options_frame, text="Data:")
        self.data_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.data_entry = tk.Entry(options_frame, width=40)
        self.data_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        # QR Color 1
        self.qr_color1_label = tk.Label(options_frame, text="QR Color 1:")
        self.qr_color1_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.qr_color1_button = tk.Button(options_frame, text="Choose Color", command=self.choose_qr_color1)
        self.qr_color1_button.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.qr_color1_preview = tk.Label(options_frame, text="", bg="black", width=4)
        self.qr_color1_preview.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.qr_color1 = "black"

        # Gradient
        self.gradient_var = tk.BooleanVar()
        self.gradient_check = tk.Checkbutton(options_frame, text="Enable Gradient", var=self.gradient_var, command=self.toggle_gradient)
        self.gradient_check.grid(row=2, column=0, columnspan=3, sticky="w", padx=5)

        # QR Color 2
        self.qr_color2_label = tk.Label(options_frame, text="QR Color 2:")
        self.qr_color2_button = tk.Button(options_frame, text="Choose Color", command=self.choose_qr_color2, state=tk.DISABLED)
        self.qr_color2_preview = tk.Label(options_frame, text="", bg="white", width=4)
        self.qr_color2 = "white"

        # BG Color
        self.bg_color_label = tk.Label(options_frame, text="Background Color:")
        self.bg_color_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.bg_color_button = tk.Button(options_frame, text="Choose Color", command=self.choose_bg_color)
        self.bg_color_button.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.bg_color_preview = tk.Label(options_frame, text="", bg="white", width=4)
        self.bg_color_preview.grid(row=4, column=2, sticky="w", padx=5, pady=5)
        self.bg_color = "white"

        # Logo
        self.logo_label = tk.Label(options_frame, text="Logo:")
        self.logo_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.logo_button = tk.Button(options_frame, text="Select Logo", command=self.select_logo)
        self.logo_button.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.logo_path_label = tk.Label(options_frame, text="No logo selected")
        self.logo_path_label.grid(row=5, column=2, sticky="w", padx=5, pady=5)
        self.logo_path = None

        # --- Preview Frame ---
        preview_frame = tk.LabelFrame(main_frame, text="Preview")
        preview_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ne")

        self.qr_image_label = tk.Label(preview_frame)
        self.qr_image_label.pack(padx=10, pady=10)

        # --- Action Frame ---
        action_frame = tk.Frame(main_frame)
        action_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.generate_button = tk.Button(action_frame, text="Generate QR Code", command=self.generate)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(action_frame, text="Save As...", command=self.save_as, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

    def choose_qr_color1(self):
        color_code = colorchooser.askcolor(title="Choose QR color 1")
        if color_code:
            self.qr_color1 = color_code[1]
            self.qr_color1_preview.config(bg=self.qr_color1)

    def choose_qr_color2(self):
        color_code = colorchooser.askcolor(title="Choose QR color 2")
        if color_code:
            self.qr_color2 = color_code[1]
            self.qr_color2_preview.config(bg=self.qr_color2)

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose background color")
        if color_code:
            self.bg_color = color_code[1]
            self.bg_color_preview.config(bg=self.bg_color)

    def select_logo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.logo_path = file_path
            self.logo_path_label.config(text=os.path.basename(file_path))

    def toggle_gradient(self):
        if self.gradient_var.get():
            self.qr_color2_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
            self.qr_color2_button.grid(row=3, column=1, sticky="w", padx=5, pady=5)
            self.qr_color2_button.config(state=tk.NORMAL)
            self.qr_color2_preview.grid(row=3, column=2, sticky="w", padx=5, pady=5)
        else:
            self.qr_color2_label.grid_remove()
            self.qr_color2_button.grid_remove()
            self.qr_color2_preview.grid_remove()

    def generate(self):
        data = self.data_entry.get()
        if not data:
            messagebox.showerror("Error", "Data cannot be empty.")
            return

        self.temp_filename = "temp_qr.png"

        try:
            if self.gradient_var.get():
                if self.logo_path:
                    generer_qr_code_avec_logo_et_degrade(data, self.temp_filename, self.logo_path, self.qr_color1, self.qr_color2, self.bg_color)
                else:
                    creer_degraded_qr(data, self.temp_filename, self.qr_color1, self.qr_color2, self.bg_color)
            else:
                if self.logo_path:
                    generer_qr_code_avec_logo(data, self.temp_filename, self.logo_path, self.qr_color1, self.bg_color)
                else:
                    generer_qr_code_personnalise(data, self.temp_filename, self.qr_color1, self.bg_color)

            self.show_qr_preview(self.temp_filename)
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {e}")

    def show_qr_preview(self, filename):
        img = Image.open(filename)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        self.qr_photo_image = ImageTk.PhotoImage(img)
        self.qr_image_label.config(image=self.qr_photo_image)

    def save_as(self):
        if not hasattr(self, 'temp_filename') or not os.path.exists(self.temp_filename):
            messagebox.showerror("Error", "No QR code generated to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")], initialfile="my_qrcode.png")
        if save_path:
            os.rename(self.temp_filename, save_path)
            messagebox.showinfo("Success", f"QR code saved to {save_path}")
            self.save_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
