import argparse
from PIL import Image
import os

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)

def resize_images_in_directory(directory, size):
    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp", ".jfif")):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, filename)
            resize_image(input_path, output_path, size)
            print(f"Resized {filename} to {size}")

def main():
    parser = argparse.ArgumentParser(description="Resize images in a directory.")
    parser.add_argument("-d", "--directory", type=str, required=True, help="The directory containing images to resize.")
    parser.add_argument("-w", "--width", type=int, required=True, help="The width to resize images to.")
    parser.add_argument("-h", "--height", type=int, required=True, help="The height to resize images to.")
    
    args = parser.parse_args()
    
    size = (args.width, args.height)
    resize_images_in_directory(args.directory, size)

if __name__ == "__main__":
    main()