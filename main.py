# main.py
from fastapi import FastAPI, Depends
from routes import router
from dependencies import get_supabase

app = FastAPI()

# Include the router and pass the Supabase client
app.include_router(router, dependencies=[Depends(get_supabase)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
