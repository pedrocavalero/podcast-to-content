import argparse
from PIL import Image

def resize_image(input_path, output_path, width, height):
    """
    Resizes an image to the specified dimensions.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the resized image file.
        width (int): Desired width of the output image.
        height (int): Desired height of the output image.
    """
    try:
        img = Image.open(input_path)
        resized_img = img.resize((width, height), Image.LANCZOS)
        resized_img.save(output_path)
        print(f"Image resized and saved to {output_path}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred during image resizing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize an image to specified dimensions.")
    parser.add_argument("input_path", type=str, help="Path to the input image file.")
    parser.add_argument("output_path", type=str, help="Path to save the resized image file.")
    parser.add_argument("--width", type=int, required=True, help="Desired width of the output image.")
    parser.add_argument("--height", type=int, required=True, help="Desired height of the output image.")

    args = parser.parse_args()

    resize_image(args.input_path, args.output_path, args.width, args.height)
