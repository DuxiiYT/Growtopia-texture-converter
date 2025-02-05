import os
import numpy as np
from collections import Counter
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

blocks = {
    "Grey Block": (220, 220, 220),
    "Black Block": (57, 57, 57),
    "White Block": (255, 255, 255),
    "Red Block": (251, 100, 93),
    "Orange Block": (254, 139, 12),
    "Yellow Block": (247, 234, 97),
    "Green Block": (112, 213, 20),
    "Aqua Block": (20, 214, 174),
    "Blue Block": (102, 177, 255),
    "Purple Block": (216, 142, 255),
    "Brown Block": (190, 145, 120),
    "Pastel Pink Block": (248, 209, 236),
    "Pastel Orange Block": (245, 223, 198),
    "Pastel Yellow Block": (243, 240, 185),
    "Pastel Green Block": (197, 242, 178),
    "Pastel Aqua Block": (178, 242, 232),
    "Pastel Blue Block": (206, 222, 247),
    "Pastel Purple Block": (231, 198, 245),
    "Dark Grey Block": (96, 96, 96),
    "Dark Red Block": (134, 0, 3),
    "Dark Orange Block": (122, 66, 0),
    "Dark Yellow Block": (129, 110, 0),
    "Dark Green Block": (0, 74, 0),
    "Dark Aqua Block": (0, 75, 42),
    "Dark Blue Block": (0, 38, 147),
    "Dark Purple Block": (92, 0, 147),
    "Dark Brown Block": (64, 36, 6)
}

block_ids = {
    "Grey Block": 164,
    "Black Block": 166,
    "White Block": 168,
    "Red Block": 170,
    "Orange Block": 172,
    "Yellow Block": 174,
    "Green Block": 176,
    "Aqua Block": 178,
    "Blue Block": 180,
    "Purple Block": 182,
    "Brown Block": 184,
    "Pastel Pink Block": 510,
    "Pastel Orange Block": 512,
    "Pastel Yellow Block": 514,
    "Pastel Green Block": 516,
    "Pastel Aqua Block": 518,
    "Pastel Blue Block": 520,
    "Pastel Purple Block": 522,
    "Dark Grey Block": 2012,
    "Dark Red Block": 2014,
    "Dark Orange Block": 2016,
    "Dark Yellow Block": 2018,
    "Dark Green Block": 2020,
    "Dark Aqua Block": 2022,
    "Dark Blue Block": 2024,
    "Dark Purple Block": 2026,
    "Dark Brown Block": 2028
}

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Growtopia Image Converter")
        self.root.geometry("")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.preview_label = ttk.Label(self.frame)
        self.preview_label.grid(row=5, column=0, columnspan=3, pady=10)

        self.preview_button = ttk.Button(self.frame, text="Show Preview", command=self.show_preview)
        self.preview_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.input_image_path = tk.StringVar()
        ttk.Label(self.frame, text="Search For Image:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_image_entry = ttk.Entry(self.frame, textvariable=self.input_image_path, width=40)
        self.input_image_entry.grid(row=0, column=1, padx=5, pady=5)
        self.input_image_button = ttk.Button(self.frame, text="Browse", command=self.load_input_image)
        self.input_image_button.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.frame, text="X Tiles ( Length ) :").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.x_tiles_entry = ttk.Entry(self.frame, width=10)
        self.x_tiles_entry.grid(row=1, column=1, padx=5, pady=5)
        self.x_tiles_entry.insert(0, "100")

        ttk.Label(self.frame, text="Y Tiles ( Width ) :").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.y_tiles_entry = ttk.Entry(self.frame, width=10)
        self.y_tiles_entry.grid(row=2, column=1, padx=5, pady=5)
        self.y_tiles_entry.insert(0, "54")

        self.convert_button = ttk.Button(self.frame, text="Convert", command=self.convert_image)
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=20)

    def load_input_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.input_image_path.set(file_path)

    def convert_image(self):
        input_image_path = self.input_image_path.get()
        x_tiles = int(self.x_tiles_entry.get())
        y_tiles = int(self.y_tiles_entry.get())

        if not input_image_path or not os.path.isfile(input_image_path):
            messagebox.showerror("Error", "Please select a valid input image.")
            return

        if x_tiles > 100:
            messagebox.showerror("Error", "Maximum number of X tiles is 100.")
            return
        if y_tiles > 54:
            messagebox.showerror("Error", "Maximum number of Y tiles is 54.")
            return
        if x_tiles == 0:
            messagebox.showerror("Error", "Minimum number of X tiles is 1.")
            return
        if y_tiles == 0:
            messagebox.showerror("Error", "Minimum number of Y tiles is 1.")
            return

        input_image = Image.open(input_image_path)
        width, height = input_image.size

        tile_width = width // x_tiles
        tile_height = height // y_tiles

        if width > (tile_width * x_tiles) or height > (tile_height * y_tiles):
            target_width = x_tiles * tile_width
            target_height = y_tiles * tile_height

            input_image = input_image.resize((target_width, target_height), Image.LANCZOS)
            width, height = input_image.size

        if tile_width == 0 or tile_height == 0:
            messagebox.showerror("Error", "Number of tiles is too high for the selected image size.")
            return

        img_data = np.array(input_image)

        image_name = os.path.splitext(os.path.basename(input_image_path))[0]

        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(output_folder, exist_ok=True)

        blocks_data_path = os.path.join(output_folder, "blocks_data.txt")
        blocks_needed_path = os.path.join(output_folder, "blocks_needed.txt")

        block_counts = Counter()

        with open(blocks_data_path, "w") as data_file, open(blocks_needed_path, "w") as blocks_needed_file:
            for y in range(y_tiles):
                for x in range(x_tiles):
                    tile = img_data[y * tile_height:(y + 1) * tile_height, x * tile_width:(x + 1) * tile_width]

                    if tile.size == 0:
                        continue

                    common_color = self.most_common_color(tile)
                    closest_block = self.find_closest_block_color(common_color)

                    block_id = block_ids[closest_block]
                    data_file.write(f"{x}, {y}, {block_id}\n")

                    block_counts[closest_block] += 1

            sorted_block_counts = sorted(block_counts.items(), key=lambda x: x[1], reverse=True)
            for block_name, count in sorted_block_counts:
                blocks_needed_file.write(f"{block_name}: {count}\n")

            messagebox.showinfo("Success", f"Conversion completed. Data saved to {output_folder}")

    def most_common_color(self, tile):
        if tile.size == 0:
            return (0, 0, 0)

        pixels = tile.reshape(-1, tile.shape[-1])
        most_common = Counter(map(tuple, pixels)).most_common(1)

        if not most_common:
            messagebox.showerror("Error", "No common color found in the tile.")
            return (0, 0, 0)

        return most_common[0][0]

    def find_closest_block_color(self, color):
        closest_block = None
        min_diff = float('inf')

        color = color[:3]

        for block_name, block_color in blocks.items():
            diff = np.linalg.norm(np.array(color) - np.array(block_color))
            if diff < min_diff:
                min_diff = diff
                closest_block = block_name

        return closest_block

    def show_preview(self):
        input_image_path = self.input_image_path.get()
        x_tiles = int(self.x_tiles_entry.get())
        y_tiles = int(self.y_tiles_entry.get())

        if not input_image_path or not os.path.isfile(input_image_path):
            messagebox.showerror("Error", "Please select a valid input image.")
            return

        input_image = Image.open(input_image_path)
        input_image = input_image.resize((x_tiles, y_tiles), Image.LANCZOS)

        img_data = np.array(input_image)
        preview_image = Image.new("RGB", (x_tiles * 10, y_tiles * 10))

        for y in range(y_tiles):
            for x in range(x_tiles):
                pixel = img_data[y, x, :3]
                closest_block = self.find_closest_block_color(tuple(pixel))

                block_image_path = os.path.join("blocks", f"{closest_block}.png")
                
                if os.path.isfile(block_image_path):
                    block_image = Image.open(block_image_path)
                    block_image = block_image.resize((10, 10), Image.NEAREST)
                    preview_image.paste(block_image, (x * 10, y * 10))

        self.tk_preview = ImageTk.PhotoImage(preview_image)
        self.preview_label.config(image=self.tk_preview)
        self.preview_label.image = self.tk_preview 

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
