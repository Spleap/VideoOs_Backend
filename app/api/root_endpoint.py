from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.image import ImageResponse
from app.services.image_service import image_service

router = APIRouter()

@router.post("", response_model=ImageResponse)
async def upload_image_root(
    file: UploadFile = File(...),
    mode: str = Form(...),
    sent_Prompt: str = Form(..., alias="sent_Prompt"),
    if_ask: int = Form(...)
):
    """
    Root level upload endpoint to match frontend '/upload' call.
    """
    is_ask_bool = True if if_ask == 1 else False
    return await image_service.process_image(file, mode, sent_Prompt, is_ask_bool)
