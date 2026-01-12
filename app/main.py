from app.routers import cars, dealers

from fastapi import FastAPI


app = FastAPI(title="Car Sales API")

app.include_router(cars.router) 
app.include_router(dealers.router)