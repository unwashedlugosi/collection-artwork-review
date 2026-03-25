import google.genai as genai
from google.genai import types
import base64, sys

client = genai.Client(api_key=" 'os.environ.get("GEMINI_API_KEY", "")")

prompt = """Generate a square app icon (1024x1024). The icon should be:
- A magnifying glass hovering over a vintage cassette tape J-card/insert
- The J-card has tiny handwritten-style text on aged paper
- The magnifying glass has a gold rim
- Dark background (near black, like #111)
- Gold and cream color palette to match a vintage music reviewer aesthetic
- Clean, modern icon style — no text, no letters
- The image must fill the entire square with NO rounded corners, NO border, NO margin
- Photorealistic style with slight retro warmth"""

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        # Write raw bytes directly
        raw = part.inline_data.data
        # Check if it's already bytes or base64 string
        if isinstance(raw, bytes):
            img_data = raw
        else:
            img_data = base64.b64decode(raw)
        
        with open("icon-1024.png", "wb") as f:
            f.write(img_data)
        
        # Verify it's a valid image
        from PIL import Image
        img = Image.open("icon-1024.png")
        print(f"Icon saved: {img.size}, {img.mode}, {img.format}")
        img.resize((180, 180), Image.LANCZOS).save("icon-180.png")
        img.resize((32, 32), Image.LANCZOS).save("favicon.png")
        print("All sizes generated")
        sys.exit(0)

print("No image generated")
sys.exit(1)
