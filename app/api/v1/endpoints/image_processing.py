from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.image import ImageResponse
from app.services.image_service import image_service

router = APIRouter()

@router.post("/process", response_model=ImageResponse)
async def process_image(
    file: UploadFile = File(...),
    mode: str = Form(...),
    sent_Prompt: str = Form(..., alias="sent_Prompt"), # Matches frontend: sent_Prompt
    if_ask: int = Form(...) # Matches frontend: 0 or 1
):
    """
    Receive an image, mode, sent_Prompt (history), and if_ask flag (0 or 1).
    if_ask=0: Summarize the image based on history.
    if_ask=1: Answer the user question (contained in prompt) based on history and image.
    """
    # Convert integer flag to boolean
    is_ask_bool = True if if_ask == 1 else False
    
    return await image_service.process_image(file, mode, sent_Prompt, is_ask_bool)
