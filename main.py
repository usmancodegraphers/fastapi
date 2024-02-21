from fastapi import FastAPI

from core.services.bookstore.bookstore_routes import router as bookstore_router
from core.services.productstore.routes import router as product_router

app = FastAPI()

app.include_router(bookstore_router)
app.include_router(product_router)
