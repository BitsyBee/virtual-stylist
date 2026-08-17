from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.clothing_item import router as clothing_router
from app.routes.recommendation import router as recommendation_router
from app.routes.favorite import router as favorite_router        
from app.routes.chat_history import router as chat_history_router 


app = FastAPI(
    title="Virtual Stylist API"
)


# Serve clothing images
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "dataset" / "images"

app.mount(
    "/images",
    StaticFiles(directory=str(IMAGE_DIR)),
    name="images"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(clothing_router)
app.include_router(recommendation_router)
app.include_router(favorite_router)          
app.include_router(chat_history_router) 


@app.get("/")
def root():
    return {
        "message": "Virtual Stylist API Running"
    }