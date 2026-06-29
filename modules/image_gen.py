import requests
import os
from datetime import datetime

SAVE_DIR = "generated_images"

os.makedirs(SAVE_DIR, exist_ok=True)

def generate_image(prompt):

    filename = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    filepath = os.path.join(
        SAVE_DIR,
        filename
    )

    url = f"https://image.pollinations.ai/prompt/{prompt}"

    response = requests.get(url)

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath