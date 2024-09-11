from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from dependencies import get_supabase

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = security, supabase: Client = get_supabase()):
    token = credentials.credentials
    try:
        user = supabase.auth.get_user(token)
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

async def auth_middleware(request: Request):
    if "authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    auth_header = request.headers["authorization"]
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    token = auth_header.split(" ")[1]
    try:
        user = await verify_token(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
        request.state.user = user
    except HTTPException:
        raise HTTPException(status_code=401, detail="Unauthorized")