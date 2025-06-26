import uvicorn
from fastapi import APIRouter, FastAPI

from api.task import router as tasks_router
from core.config import settings

app = FastAPI()

combined_router = APIRouter(prefix="/api/v1")
combined_router.include_router(tasks_router)

app.include_router(combined_router)

if __name__ == "__main__":
    uvicorn.run("web_server:app", host=settings.run.host, port=settings.run.port, reload=True)
