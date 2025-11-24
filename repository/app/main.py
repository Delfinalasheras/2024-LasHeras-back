from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI()

# Allow CORS for the frontend
origins = [
    "http://localhost:3000",
    "https://2024-ranchoaparte-front-ivory.vercel.app",
    "http://localhost:4201",
    "https://2024-messidepaul-front.vercel.app"


]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

# Your routes here...
app.include_router(router)