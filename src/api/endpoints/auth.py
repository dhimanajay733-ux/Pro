from fastapi import APIRouter, Request
from src.schemas.auth import LoginRequest, LoginResponse
from src.services.auth_service import AuthService
from src.core.limiter import limiter  
from fastapi import Header

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")   
def login(request: Request, data: LoginRequest):
    return auth_service.login(data)

@router.post("/logout")
def logout(authorization: str = Header()):
    token = authorization.split(" ")[1]
    return auth_service.logout(token)