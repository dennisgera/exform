from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth
from app.core.config import settings

app = FastAPI(
    title="Exercise Form Analysis API",
    description="API for analyzing exercise form using AI",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to Exercise Form Analysis API"}

# Import and include routers
# We'll add these as we build them
# from app.api.endpoints import users, videos, auth
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(videos.router, prefix="/videos", tags=["videos"])