
import os
import argparse
import base64
from dotenv import load_dotenv
from openai import OpenAI
import requests

def generate_image(prompt, output_path, model="gpt-image-1", size="1024x1024"):
    """
    Generates an image from a text prompt using OpenAI's DALL-E API.

    Args:
        prompt: The text prompt to generate the image from.
        output_path: The path to save the generated image to.
        model: The model to use for image generation. Can be "dall-e-3" or "gpt-image-1".
    """
    load_dotenv() # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file or environment variables.")
        return

    client = OpenAI(api_key=api_key)

    try:
        supported_sizes = {
            "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"],
            "gpt-image-1": ["256x256", "512x512", "1024x1024", "1536x1024"]
        }

        if model not in supported_sizes:
            raise ValueError(f"Unsupported model: {model}")

        if size not in supported_sizes[model]:
            print(f"Warning: Provided size '{size}' is not supported for model '{model}'. Using default size '{supported_sizes[model][0]}'.")
            size = supported_sizes[model][0] # Use the first supported size as default

        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size, # Use the passed/validated size
            quality="hd" if model == "dall-e-3" else "high",
            n=1,
        )

        if model == "gpt-image-1": # DALL-E 2 returns base64 for gpt-image-1
            b64_json = response.data[0].b64_json
            if b64_json:
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(b64_json))
                print(f"Image saved to {output_path}")
            else:
                print("No base64 image data found in the API response.")
        else: # DALL-E 3 returns a URL
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
    parser.add_argument("--model", type=str, default="gpt-image-1", choices=["dall-e-3", "gpt-image-1"], help="The model to use for image generation.")
    parser.add_argument("--size", type=str, default="1024x1024", help="The size of the generated image (e.g., '1024x1024', '1792x1024').")
    args = parser.parse_args()

    generate_image(args.prompt, args.output_path, args.model, args.size)
