from fastapi import Header, HTTPException, Depends
from typing import Optional
import jwt
import os
import hmac
import bcrypt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secret key from environment
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")

# Clock skew tolerance in seconds (60 seconds)
CLOCK_SKEW = 60


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT access token for a user."""
    payload = {
        "user_id": user_id,
        "email": email,
    }
    token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm="HS256")
    return token


async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract and verify JWT token, return user_id.
    
    This dependency is used by all protected endpoints to ensure
    the request is authenticated and to extract the user's ID.
    
    Args:
        authorization: Authorization header value (format: "Bearer {token}")
        
    Returns:
        str: The authenticated user's user_id
        
    Raises:
        HTTPException: 401 Unauthorized if token is missing, invalid, or expired
        
    Usage:
        @app.get("/api/tasks")
        async def list_tasks(user_id: str = Depends(get_current_user)):
            # user_id is guaranteed to be authenticated
            ...
    """
    
    # Step 1: Check Authorization header exists
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Authorization header is required"
            }
        )
    
    # Step 2: Parse Bearer token
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid token format. Use: Bearer {token}"
            }
        )
    
    token = parts[1]
    
    # Step 3: Verify token signature and expiration
    try:
        # Decode and verify the token
        # PyJWT automatically checks expiration when 'exp' claim exists
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"],
            options={
                "verify_exp": True,
                "verify_iat": True
            },
            leeway=CLOCK_SKEW  # Allow 60 seconds clock skew
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Token has expired"
            }
        )
    except jwt.InvalidTokenError as e:
        # Handle invalid signature, malformed token, etc.
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid token"
            }
        )
    
    # Step 4: Extract user_id from payload
    # Support both 'user_id' and 'sub' claims
    user_id = payload.get("user_id") or payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid token: missing user_id"
            }
        )
    
    # Step 5: Return authenticated user_id
    return str(user_id)
