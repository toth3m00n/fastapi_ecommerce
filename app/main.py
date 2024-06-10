from uuid import uuid4
from loguru import logger

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.middlewares import TimingMiddleware
from app.routes import category, product, auth, permission

logger.add("info.log", format="Log: [{extra[log_id]}:{time} - {level} - {message} ", level="INFO", enqueue=True)

app = FastAPI(version='0.0.1')
app.add_middleware(TimingMiddleware)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        try:
            response = await call_next(request)
            if response.status_code in [401, 402, 403, 404]:
                logger.warning(f"Request to {request.url.path} failed")
            else:
                logger.info('Successfully accessed ' + request.url.path)
        except Exception as ex:
            logger.error(f"Request to {request.url.path} failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        return response

@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(permission.router)
