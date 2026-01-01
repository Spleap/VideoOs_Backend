from fastapi.testclient import TestClient
from app.main import app
from PIL import Image
import io

client = TestClient(app)

def test_process_image_with_mode():
    # Create a dummy image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    files = {'file': ('test.png', img_byte_arr, 'image/png')}
    data = {'mode': 'test_mode'}

    response = client.post("/api/v1/image/process", files=files, data=data)
    
    print(response.json())
    assert response.status_code == 200
    assert response.json()['message'] == "Image processed successfully with mode 'test_mode'. Dimensions: 100x100"

if __name__ == "__main__":
    test_process_image_with_mode()
    print("Test passed!")
