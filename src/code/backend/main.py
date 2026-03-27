from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import health, upload

app = FastAPI(title="Medical Segmentation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # порт React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(health.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Medical API is running", "docs": "/docs"}