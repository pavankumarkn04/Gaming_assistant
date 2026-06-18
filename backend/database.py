from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "stan_gaming.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PlayerSession(Base):
    __tablename__ = "player_sessions"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, index=True)
    game = Column(String(20), nullable=False)
    stats_json = Column(Text, nullable=False)
    analysis_json = Column(Text, nullable=False)
    performance_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
