# VideoOs Backend

This is an enterprise-grade backend service built with FastAPI.

## Features

- **Image Processing**: Upload and process images.
- **Data Processing**: Process JSON data.
- **Enterprise Structure**: Scalable folder structure.
- **Logging**: Advanced logging with Loguru.
- **Configuration**: Environment-based configuration with Pydantic.

## Setup

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

## API Documentation

Once the server is running, you can access the interactive API docs at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints

- `POST /api/v1/image/process`: Upload an image file.
- `POST /api/v1/data/process`: Send JSON data.
