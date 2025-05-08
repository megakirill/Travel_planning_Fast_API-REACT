from fastapi import FastAPI
from api import api_router
app = FastAPI()

@app.get("/{id}")
async def root():
    return {"message": "Hello World"}
app.include_router(api_router, prefix="/api")



