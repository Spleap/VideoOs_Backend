from fastapi import APIRouter
from app.api.v1.endpoints import image_processing

api_router = APIRouter()

# Matches frontend call: /upload (although frontend uses base URL + /upload, 
# in FastAPI structure it is usually /api/v1/upload. 
# But if frontend calls apiClient.post("/upload"), and apiClient base is http://host:8000, 
# then the full URL is http://host:8000/upload.
# However, this file defines routes under /api/v1 prefix in main.py.
# We should probably change the prefix here or change main.py to serve /upload at root if that's what frontend expects.
# Given the user context "FastAPI", usually /docs shows /api/v1/....
# BUT the frontend code shows: const API_BASE_URL = "http://10.60.185.80:8000"; apiClient.post("/upload", ...)
# This implies the POST request goes to http://10.60.185.80:8000/upload
# So we need to expose /upload at the root level in main.py, OR tell user to change frontend.
# Since I am "Backend" dev, I should probably adapt to frontend or create a route that matches.
# Let's add an alias or a root router in main.py, but here in v1/api.py we keep standard structure.
# Wait, I will modify main.py to include a root router for /upload to match frontend perfectly.

api_router.include_router(image_processing.router, prefix="/image", tags=["image"])
