
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
import requests

def generate_image(prompt, output_path):
    """
    Generates an image from a text prompt using OpenAI's DALL-E API.

    Args:
        prompt: The text prompt to generate the image from.
        output_path: The path to save the generated image to.
    """
    load_dotenv() # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file or environment variables.")
        return

    client = OpenAI(api_key=api_key)

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high",
            n=1,
        )

        image_url = response.data[0].url
        if image_url:
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(image_response.content)
            print(f"Image saved to {output_path}")
        else:
            print("No image URL found in the API response.")

    except Exception as e:
        print(f"Error generating image with OpenAI: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an image from a text prompt using OpenAI's DALL-E API.")
    parser.add_argument("prompt", type=str, help="The text prompt to generate the image from.")
    parser.add_argument("output_path", type=str, help="The path to save the generated image to.")
    args = parser.parse_args()

    generate_image(args.prompt, args.output_path)
