from fastapi import FastAPI
from shared.shared.services.git_service import checkout_repo

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}