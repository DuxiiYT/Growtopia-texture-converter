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

| Before Conversion | Preview | In-game showcase |
| ![Original Image](https://github.com/user-attachments/assets/f0674205-3eb2-43ef-ab02-7ff9edf18c7b)
| ![Previewed Image](https://github.com/user-attachments/assets/e5a6e50c-ff91-43ef-8db0-384e585a93b8)
| ![In-game Image](https://github.com/user-attachments/assets/6cff28ae-b71f-4e38-8de4-25912fba9bcc)



