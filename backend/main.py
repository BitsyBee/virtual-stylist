from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Virtual Stylist API"
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Virtual Stylist API Running"
    }