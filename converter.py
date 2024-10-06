import os
import numpy as np
from collections import Counter
from PIL import Image
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

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Growtopia Image Converter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.input_image_path = tk.StringVar()
        ttk.Label(self.frame, text="Search For Image:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_image_entry = ttk.Entry(self.frame, textvariable=self.input_image_path, width=40)
        self.input_image_entry.grid(row=0, column=1, padx=5, pady=5)
        self.input_image_button = ttk.Button(self.frame, text="Browse", command=self.load_input_image)
        self.input_image_button.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.frame, text="X Tiles ( Length ) :").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.x_tiles_entry = ttk.Entry(self.frame, width=10)
        self.x_tiles_entry.grid(row=1, column=1, padx=5, pady=5)
        self.x_tiles_entry.insert(0, "99")

        ttk.Label(self.frame, text="Y Tiles ( Width ) :").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.y_tiles_entry = ttk.Entry(self.frame, width=10)
        self.y_tiles_entry.grid(row=2, column=1, padx=5, pady=5)
        self.y_tiles_entry.insert(0, "53")

        self.convert_button = ttk.Button(self.frame, text="Convert", command=self.convert_image)
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=20)
        self.convert_button.bind("<Enter>", self.on_hover)
        self.convert_button.bind("<Leave>", self.on_leave)

        self.block_images = {}
        self.load_block_images()

    def on_hover(self, event):
        event.widget['style'] = 'TButton'

    def on_leave(self, event):
        event.widget['style'] = 'TButton'

    def load_block_images(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        blocks_dir = os.path.join(script_dir, "blocks")

        for block_name in blocks.keys():
            image_path = os.path.join(blocks_dir, f"{block_name}.png")
            if os.path.isfile(image_path):
                self.block_images[block_name] = Image.open(image_path)

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

        if x_tiles > 99:
            messagebox.showerror("Error", "Maximum number of X tiles is 99.")
            return
        if y_tiles > 53:
            messagebox.showerror("Error", "Maximum number of Y tiles is 53.")
            return

        input_image = Image.open(input_image_path)
        width, height = input_image.size

        if width > 5000 or height > 5000:
            messagebox.showerror("Error", "Image resolution is too high. Please select an image with lower resolution.")
            return

        tile_width = width // x_tiles
        tile_height = height // y_tiles

        if tile_width == 0 or tile_height == 0:
            messagebox.showerror("Error", "Number of tiles is too high for the selected image size.")
            return

        output_image = Image.new("RGB", (width, height))

        img_data = np.array(input_image)

        for y in range(y_tiles):
            for x in range(x_tiles):
                box = (x * tile_width, y * tile_height, (x + 1) * tile_width, (y + 1) * tile_height)
                tile = img_data[y * tile_height:(y + 1) * tile_height, x * tile_width:(x + 1) * tile_width]

                if tile.size == 0:
                    continue

                common_color = self.most_common_color(tile)
                closest_block = self.find_closest_block_color(common_color)

                block_image = self.block_images[closest_block].resize((tile_width, tile_height), Image.LANCZOS)
                output_image.paste(block_image, box)

        base_name = os.path.splitext(os.path.basename(input_image_path))[0]
        output_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{base_name}_converted.png")
        
        output_image.save(output_image_path)
        messagebox.showinfo("Success", f"Conversion completed. Output image saved to {output_image_path}")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()