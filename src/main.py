from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from src.api.endpoints import user, auth
from src.core.limiter import limiter
from src.databases.database import Base, engine, ensure_schema

app = FastAPI()

# ✅ CORS (keep only if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # simplified
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  DEBUG 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )

ensure_schema()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

#  Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")