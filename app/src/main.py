import uvicorn
from fastapi import FastAPI
from src.routes import router

app = FastAPI(
    title="Wacef test - LLM Structured Data API",
    description="Data classification and extraction API",
    version="1.0.0",
)
app.include_router(router, prefix="/api/v1")


@app.get("/")
def welcome_msg():
    return {
        "app_name": app.title,
        "version": app.version,
        "status": "online",
        "message": f"Welcome to the {app.title} API documentation!",
    }


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
