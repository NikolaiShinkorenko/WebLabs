from app.routers import cars, dealers

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Car Sales API")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(cars.router) 
app.include_router(dealers.router)

@app.get("/")
def reed_root():
    return FileResponse("static/index.html")