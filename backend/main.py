from fastapi import FastAPI

app = FastAPI(title="Virtual Stylist API")

@app.get("/")
def root():
    return {"message": "Virtual Stylist API Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}