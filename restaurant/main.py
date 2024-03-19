from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import user, order

app = FastAPI(port=8080)  # FastAPI app initialization
app.include_router(order.router)  # initialize order router
app.include_router(user.router)  # initialize user router
Base.metadata.create_all(engine)  # migrating all models
