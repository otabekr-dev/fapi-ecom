from fastapi import FastAPI

from apps.users.routers import router as users_router
from apps.sellers.router import router as sellers_router
from apps.products.routers import c_router, p_router
from apps.carts.routers import router as cart_router

app = FastAPI()

app.include_router(users_router)
app.include_router(sellers_router)
app.include_router(c_router)
app.include_router(p_router)
app.include_router(cart_router)

@app.get('/health')
def health():
    return {'status':'healthy'}
