from fastapi import UploadFile
from PIL import Image
from io import BytesIO
import base64
import httpx
import json
from app.schemas.image import ImageResponse
from app.core.exceptions import ImageProcessingError
from app.utils.logger import logger
from app.core.config import settings

import os

class ImageService:
    async def process_image(self, file: UploadFile, mode: str, prompt: str, if_ask: bool) -> ImageResponse:
        logger.info(f"Processing image: {file.filename} with mode: {mode}, if_ask: {if_ask}")
        
        if not file.content_type.startswith("image/"):
            raise ImageProcessingError(detail="File is not an image")

        contents = await file.read()
        
        try:
            # Check image validity
            image = Image.open(BytesIO(contents))
            width, height = image.size
            format = image.format
            
            # Load system prompt from markdown file based on mode and if_ask
            # Structure: app/prompts/{mode}/{mode}_{type}.md
            prompt_type = "answer" if if_ask else "summary"
            prompt_file_path = os.path.join("app", "prompts", mode, f"{mode}_{prompt_type}.md")
            system_prompt = ""
            
            if os.path.exists(prompt_file_path):
                try:
                    with open(prompt_file_path, "r", encoding="utf-8") as f:
                        system_prompt = f.read()
                    logger.info(f"Loaded system prompt from {prompt_file_path}")
                except Exception as e:
                    logger.warning(f"Failed to read prompt file {prompt_file_path}: {e}")
            else:
                logger.warning(f"Prompt file not found: {prompt_file_path}.")

            # Construct Final Prompt
            history_context = prompt if prompt else ""
            
            if if_ask:
                # Ask Mode: History + Question is already in 'prompt'. 
                # System prompt + History/Question
                final_prompt = f"{system_prompt}\n\n{history_context}".strip()
            else:
                # Summary Mode: History is in 'prompt'.
                # System prompt + History + Explicit Summary Instruction
                # Note: The system prompt (summary version) should already contain instructions to summarize, 
                # but we can add a generic reinforcement here if needed, or rely on the MD file.
                # Let's rely mainly on the MD file + Context.
                final_prompt = f"{system_prompt}\n\nContext:\n{history_context}".strip()
            
            if not final_prompt:
                final_prompt = "Describe this image in detail."

            return await self._process_gemini(contents, file.filename, width, height, format, final_prompt)

        except ImageProcessingError:
            raise
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise ImageProcessingError(detail=f"Failed to process image: {str(e)}")

    async def _process_gemini(self, image_bytes: bytes, filename: str, width: int, height: int, fmt: str, prompt: str) -> ImageResponse:
        logger.info("Calling Gemini Flash Model...")
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Logic 2: Gemini Flash
        # Switch to non-streaming endpoint for simplicity and stability if stream hangs
        # URL: https://www.dmxapi.cn/v1beta/models/gemini-2.5-flash:generateContent
        # Removing alt=sse to use standard JSON response
        url = f"{settings.DMXAPI_GEMINI_BASE_URL}/models/gemini-2.5-flash:generateContent?key={settings.DMXAPI_KEY}"
        
        payload = {
            "contents": [{
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": f"image/{fmt.lower() if fmt else 'jpeg'}",
                            "data": encoded_image
                        }
                    },
                    {"text": prompt}
                ]
            }]
        }
        
        try:
            # Increase timeout significantly for image processing
            async with httpx.AsyncClient(timeout=120.0) as client:
                logger.info("Sending request to Gemini API (non-stream)...")
                response = await client.post(url, headers={"Content-Type": "application/json"}, json=payload)
                
                if response.status_code != 200:
                    logger.error(f"Gemini API Error: Status {response.status_code}, Body: {response.text}")
                    response.raise_for_status()

                result = response.json()
                logger.info("Received response from Gemini API")
                
                full_text = ""
                if 'candidates' in result:
                    for candidate in result['candidates']:
                        if 'content' in candidate and 'parts' in candidate['content']:
                            for part in candidate['content']['parts']:
                                if 'text' in part:
                                    full_text += part['text']
                                    
                return ImageResponse(
                    filename=filename,
                    size=len(image_bytes),
                    format=fmt or "UNKNOWN",
                    message=full_text
                )
 
        except Exception as e:
            logger.error(f"Gemini Error: {str(e)}")
            raise ImageProcessingError(detail=f"Gemini processing failed: {str(e)}")

image_service = ImageService()
