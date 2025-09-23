from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from typing import Dict, Any
from app.config import SUPABASE_JWT_SECRET

security = HTTPBearer(auto_error=True)
ALGORITHM = "HS256"  # Supabase default uses HS256 with project JWT_SECRET

def verify_supabase_jwt(token: str) -> Dict[str, Any]:
    try:
        # Debug: Check if JWT secret is loaded
        if not SUPABASE_JWT_SECRET:
            raise HTTPException(status_code=401, detail="Invalid token: JWT secret not configured")
        
        # Now verify the token with proper parameters
        payload = jwt.decode(
            token, 
            key=SUPABASE_JWT_SECRET, 
            algorithms=[ALGORITHM],
            audience="authenticated"
        )
        
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    token = creds.credentials
    return verify_supabase_jwt(token)