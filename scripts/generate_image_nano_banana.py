import os
import argparse
import base64
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import io

def generate_image(prompt, output_path, model_name="gemini-2.5-flash-image", reference_image_path="workflows/Foto-3x4.jpg", aspect_ratio="16:9"):
    """
    Generates an image from a text prompt and a reference image using Google's Gemini API (google-genai SDK).

    Args:
        prompt: The text prompt to generate the image from.
        output_path: The path to save the generated image to.
        model_name: The model to use (default: "gemini-2.5-flash-image").
        reference_image_path: Path to the reference image (e.g., user's photo).
        aspect_ratio: Aspect ratio of the generated image (default: "16:9").
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file or environment variables.")
        print("Please get an API key from https://aistudio.google.com/ and set it.")
        return

    client = genai.Client(api_key=api_key)

    try:
        inputs = [prompt]
        
        if reference_image_path:
            if os.path.exists(reference_image_path):
                print(f"Loading reference image from: {reference_image_path}")
                try:
                    img = Image.open(reference_image_path)
                    inputs.append(img)
                except Exception as e:
                    print(f"Error loading reference image: {e}")
            else:
                print(f"Warning: Reference image not found at {reference_image_path}. Proceeding with text only.")

        print(f"Generating image with model: {model_name} (Aspect Ratio: {aspect_ratio})...")
        
        try:
            # Configure aspect ratio
            image_config = types.ImageConfig(aspect_ratio=aspect_ratio)
            config = types.GenerateContentConfig(image_config=image_config)
            
            response = client.models.generate_content(
                model=model_name,
                contents=inputs,
                config=config
            )
        except Exception as e:
            if "429" in str(e):
                print("\nError: Quota exceeded (429).")
                print("You may have hit the rate limit for this model.")
                print("Please check your plan and billing details at https://aistudio.google.com/")
                return
            else:
                raise e
        
        # Check if response contains an image
        image_saved = False
        
        # Inspect response structure for google-genai SDK
        # Usually response.candidates[0].content.parts[0].inline_data
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.inline_data:
                            mime_type = part.inline_data.mime_type
                            if mime_type.startswith('image/'):
                                image_data = part.inline_data.data
                                # In google-genai, data might be bytes or base64 string?
                                # Usually bytes if it's decoded, or we need to check.
                                # Pydantic model usually keeps it as bytes if defined as bytes, or str.
                                # Let's assume bytes for now or handle both.
                                if isinstance(image_data, str):
                                    image_data = base64.b64decode(image_data)
                                
                                with open(output_path, "wb") as f:
                                    f.write(image_data)
                                print(f"Image saved to {output_path}")
                                image_saved = True
                                break
                    if image_saved: break
                
        if not image_saved:
            print("No image generated. Response text:")
            print(response.text)

    except Exception as e:
        print(f"Error generating image with Gemini: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an image using Google's Gemini API.")
    parser.add_argument("prompt", type=str, help="The text prompt to generate the image from.")
    parser.add_argument("output_path", type=str, help="The path to save the generated image to.")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash-image", help="The model to use (default: gemini-2.5-flash-image).")
    parser.add_argument("--reference_image", type=str, default="workflows/Foto-3x4.jpg", help="Path to reference image.")
    parser.add_argument("--aspect_ratio", type=str, default="16:9", help="Aspect ratio (default: 16:9).")
    
    args = parser.parse_args()

    generate_image(args.prompt, args.output_path, args.model, args.reference_image, args.aspect_ratio)
