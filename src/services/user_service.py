from src.databases.session import SessionLocal
from src.models.user import User
from sqlalchemy.exc import IntegrityError
from src.core.exceptions import EmailAlreadyExistsException
from src.core.security import hash_password


class UserService:

    def create_user(self, data):
        db = SessionLocal()

        try:
         
            existing_user = db.query(User).filter(User.email == data.email).first()
            if existing_user:
                raise EmailAlreadyExistsException("Email already exists")

            
            new_user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                password=hash_password(data.password)  
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "message": "User created successfully",
            }

        except IntegrityError:
            db.rollback()  
            raise EmailAlreadyExistsException("Email already exists")

        finally:
            db.close() 