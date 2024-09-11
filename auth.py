from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from supabase import Client
from dependencies import get_supabase
from typing import Optional, Dict, Any

auth_router = APIRouter()

# Define request models
class UserCredentials(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

# Define API endpoints
@auth_router.post("/signup")
async def api_sign_up(credentials: UserCredentials, profile: UserProfile, supabase: Client = Depends(get_supabase)):
    try:
        # Sign up the user
        auth_response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password,
            "options": {
                "data": profile.dict(exclude_none=True)
            }
        })
        
        if auth_response.user:
            # Create member in the members table
            member_data = {
                "id": auth_response.user.id,
                "email": credentials.email,
                "name": profile.full_name or credentials.email.split('@')[0]  # Use email username if full_name is not provided
            }
            member_response = supabase.table('members').insert(member_data).execute()
            
            if member_response.data:
                return {"message": "Sign up successful", "user": auth_response.user, "member": member_response.data[0]}
            else:
                # If member creation fails, delete the auth user
                supabase.auth.admin.delete_user(auth_response.user.id)
                raise HTTPException(status_code=400, detail="Failed to create member")
        else:
            raise HTTPException(status_code=400, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during sign up: {str(e)}")

@auth_router.post("/signin")
async def api_sign_in(credentials: UserCredentials, supabase: Client = Depends(get_supabase)):
    try:
        auth_response: Dict[str, Any] = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        if not auth_response.user or not auth_response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "message": "Sign in successful",
            "user": auth_response.user,
            "access_token": auth_response.session.access_token
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during sign in: {str(e)}")

@auth_router.post("/signout")
async def api_sign_out(supabase: Client = Depends(get_supabase), authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    try:
        supabase.auth.sign_out()
        return {"message": "Sign out successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during sign out: {str(e)}")

@auth_router.get("/members/{user_id}")
async def api_get_user_profile(user_id: str, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.from_('profiles').select("*").eq('id', user_id).execute()
        if response.data:
            return {"profile": response.data[0]}
        else:
            raise HTTPException(status_code=404, detail="User profile not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching user profile: {str(e)}")

@auth_router.post("/members/{user_id}")
async def api_create_user_profile(user_id: str, profile: UserProfile, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.from_('profiles').insert(profile.dict(exclude_unset=True)).execute()
        if response.data:
            return {"profile": response.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Failed to create user profile")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user profile: {str(e)}")

@auth_router.put("/members/{user_id}")
async def api_update_user_profile(user_id: str, profile: UserProfile, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.from_('profiles').update(profile.dict(exclude_unset=True)).eq('id', user_id).execute()
        if response.data:
            return {"profile": response.data[0]}
        else:
            raise HTTPException(status_code=404, detail="User profile not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user profile: {str(e)}")
