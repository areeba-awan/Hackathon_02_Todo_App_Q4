from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr, Field

from db import get_session
from models import User
from auth import hash_password, verify_password, create_access_token

# Create router with /api/auth prefix
router = APIRouter(prefix="/api/auth", tags=["authentication"])


# =============================================================================
# Request/Response Schemas
# =============================================================================

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str
    user: dict


# =============================================================================
# POST /api/auth/register - Register a new user
# =============================================================================

@router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Creates a new user with the provided email, password, and name.
    Returns a JWT token for immediate authentication.
    """
    # Check if user already exists
    statement = select(User).where(User.email == request.email)
    result = session.exec(statement)
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "USER_EXISTS",
                "message": "User with this email already exists"
            }
        )

    # Hash password and create user
    hashed_password = hash_password(request.password)

    user = User(
        email=request.email,
        name=request.name,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT token
    token = create_access_token(str(user.id), user.email)

    return AuthResponse(
        token=token,
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    )


# =============================================================================
# POST /api/auth/login - Login existing user
# =============================================================================

@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Login with email and password.

    Verifies credentials and returns a JWT token for authentication.
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    result = session.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        )

    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        )

    # Create JWT token
    token = create_access_token(str(user.id), user.email)

    return AuthResponse(
        token=token,
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    )
