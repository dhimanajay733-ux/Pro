from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import settings

engine = create_engine(settings.DB_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def ensure_schema():
    inspector = inspect(engine)

    if "users" in inspector.get_table_names():
        columns = [column["name"] for column in inspector.get_columns("users")]
        if "password" not in columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN password VARCHAR(255)"))
    else:
        Base.metadata.create_all(bind=engine)
