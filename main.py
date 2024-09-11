# main.py
from fastapi import FastAPI, Depends
from routes import books_router
from auth import auth_router
from dependencies import get_supabase
from fastapi.middleware.cors import CORSMiddleware
from middleware import auth_middleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Include the routers with their respective prefixes
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Add global middleware
app.middleware("http")(auth_middleware)

# Implement CORS to control allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("RENDER_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
