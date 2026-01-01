from pydantic import BaseModel

class ImageResponse(BaseModel):
    filename: str
    size: int
    format: str
    message: str
    # Add other fields as needed
