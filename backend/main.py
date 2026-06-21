from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.clothing_item import router as clothing_router

app = FastAPI(
    title="Virtual Stylist API"
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(clothing_router)


@app.get("/")
def root():
    return {
        "message": "Virtual Stylist API Running"
    }