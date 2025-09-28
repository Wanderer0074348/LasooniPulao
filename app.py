from fastapi import FastAPI

from src.controllers.controllers import router
from src.database.db import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)
