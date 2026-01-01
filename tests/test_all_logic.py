import pytest
from fastapi.testclient import TestClient
from app.main import app
from PIL import Image, ImageDraw
import io
import os

client = TestClient(app)

# User provided path
TEST_IMAGE_PATH = r"C:\Users\splea\Pictures\Screenshots\屏幕截图 2025-12-27 144644.png"

def get_test_image_bytes():
    if os.path.exists(TEST_IMAGE_PATH):
        print(f"Loading test image from: {TEST_IMAGE_PATH}")
        with open(TEST_IMAGE_PATH, "rb") as f:
            return f.read()
    else:
        print(f"Warning: Test image not found at {TEST_IMAGE_PATH}. Using dummy image.")
        return create_dummy_image_with_text()

def create_dummy_image_with_text(text="Hello World"):
    # Create a white image
    img = Image.new('RGB', (200, 100), color='white')
    # Since we might not have fonts, we won't draw text, just return the image.
    # OCR might return empty, but the API call should succeed.
    # To make it slightly more realistic, let's just use a solid color.
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

def test_logic_2_gemini_flash():
    print("\nTesting Gemini Flash - Code Assist Mode...")
    img_bytes = get_test_image_bytes()
    files = {'file': ('test_gemini.png', img_bytes, 'image/png')}
    
    # 1. Ask Mode
    print("  -> Testing Ask Mode (Answer Prompt)...")
    data_ask = {
        'mode': 'code_assist',
        'sent_Prompt': 'History: User asked for code review.\nUser: What does this code do?',
        'if_ask': 1
    }
    
    # Testing the new root endpoint /upload to match frontend
    response = client.post("/upload", files=files, data=data_ask)
    
    if response.status_code != 200:
         print(f"Error Detail: {response.text}")
    assert response.status_code == 200
    json_resp = response.json()
    print(f"     Response: {json_resp['message'][:100]}...")
    
    # 2. Summary Mode
    print("  -> Testing Summary Mode (Summary Prompt)...")
    
    # Reset file pointer or create new file tuple (safest)
    files = {'file': ('test_gemini.png', img_bytes, 'image/png')}
    
    data_summary = {
        'mode': 'code_assist',
        'sent_Prompt': 'History: Previous analysis done.',
        'if_ask': 0
    }
    
    response = client.post("/upload", files=files, data=data_summary)
    assert response.status_code == 200
    json_resp = response.json()
    print(f"     Response: {json_resp['message'][:100]}...")
    
    print("Gemini Flash Code Assist Mode Passed!")

if __name__ == "__main__":
    try:
        test_logic_2_gemini_flash()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTests Failed: {e}")
        exit(1)
