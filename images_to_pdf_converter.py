"""
Images to PDF Converter

Converts a directory of image files (.png, .jpg, .jpeg) to a single PDF file.
Usage: python images_to_pdf_converter.py <image_directory>
"""

import os
import sys
from PIL import Image

def images_to_pdf(folder_path, output_pdf_path):
    # Get a sorted list of image files from the folder
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    if not image_files:
        print("No image files found in the folder.")
        return

    # Open the images
    image_list = []
    for file_name in image_files:
        file_path = os.path.join(folder_path, file_name)
        img = Image.open(file_path).convert('RGB')
        image_list.append(img)

    # Save all images to a single PDF
    first_image = image_list.pop(0)
    first_image.save(output_pdf_path, save_all=True, append_images=image_list)
    print(f"PDF created successfully: {output_pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python images_to_pdf_converter.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"The specified path does not exist or is not a directory: {folder_path}")
        sys.exit(1)

    output_pdf_path = os.path.join(folder_path, "output.pdf")
    images_to_pdf(folder_path, output_pdf_path) 