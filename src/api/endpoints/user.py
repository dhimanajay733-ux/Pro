from fastapi import APIRouter
from src.schemas.user import UserCreate        
from src.services.user_service import UserService   

router = APIRouter()

user_service = UserService()   

@router.post("/create")
def create_user(data: UserCreate):
    return user_service.create_user(data) 