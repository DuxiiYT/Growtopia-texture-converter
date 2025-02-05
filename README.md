# Growtopia Image Converter

This project allows you to convert images into block-based representations for use in the game **Growtopia**. It replaces each section of the original image with the closest matching Growtopia block, resulting in an image composed of tiles.
Full Credits to xMandq!!!

## Changes

- Added a "Show Preview" button (May not be the same as in-game, will be fixed soon.
- Added a .lua file which actually starts building it. (Some features only work in CreativePS)
- Made it nicer
  
## Features

- Converts images into Growtopia tile/block grids.
- Automatically resizes images to fit within the 99x53 tile grid size limit.
- Color matching algorithm to find the closest Growtopia block for each section.
- Supports multiple block types for more accurate representations.
- Currently only works if you have Long Place!

## Installation

1. Save all files from the repository into the same folder on your machine.
2. Open a terminal or command prompt and navigate to that folder.
3. Run the following command to install the necessary dependencies:

   ```bash
   pip install -r requirements.txt

| Before Conversion | After Conversion |
| --- | --- |
| ![Original Image](https://github.com/user-attachments/assets/f1d71edb-50f7-4bf5-9738-7a096c4cbe0a) | ![Converted Image](https://github.com/user-attachments/assets/9d0ee027-b171-4fc2-a439-b0b15c3660b1) |
