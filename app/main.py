from fastapi import FastAPI
from app.routes import category, product, auth, permission

app = FastAPI(version='0.0.1')


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(permission.router)
