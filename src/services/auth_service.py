from src.core.security import create_access_token, verify_password
from src.core.logger import logger
from src.core.exceptions import InvalidCredentialsException
from src.core.token_blacklist import blacklisted_tokens
from src.databases.session import SessionLocal
from src.models.user import User

class AuthService:

    def login(self, data):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == data.email).first()
            if not user:
                logger.warning(f"Invalid email attempt: {data.email}")
                raise InvalidCredentialsException()

            if not verify_password(data.password, user.password):
                logger.warning("Wrong password attempt")
                raise InvalidCredentialsException()

            token = create_access_token({"sub": user.email})

            logger.info(f"User logged in successfully: {data.email}")

            return {
                "access_token": token,
                "token_type": "bearer"
            }
        finally:
            db.close()

    def logout(self, token: str):

        blacklisted_tokens.add(token)

        logger.info("User logged out successfully")

        return {"message": "Logged out successfully"}