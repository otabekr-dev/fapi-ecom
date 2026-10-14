from fastapi import FastAPI

from apps.users.routers import router as users_router
from apps.sellers.router import router as sellers_router

app = FastAPI()

app.include_router(users_router)
app.include_router(sellers_router)

@app.get('/health')
def health():
    return {'status':'healthy'}
