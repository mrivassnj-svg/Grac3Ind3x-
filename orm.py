# SQLAchemy ORM table
# orm.py
# -------------------
# SQLAlchemy ORM mapping for mood_entries table

from sqlalchemy import Column, Integer, Float, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class MoodEntryORM(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Text, nullable=False, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    q1 = Column(Integer)
    q2 = Column(Integer)
    q3 = Column(Integer)
    q4 = Column(Integer)
    q5 = Column(Integer)
    q6 = Column(Integer)
    q7 = Column(Integer)
    q8 = Column(Integer)
    q9 = Column(Integer)
    q10 = Column(Integer)

    fill_word = Column(Text)
    raw_score = Column(Integer)
    weighted_score = Column(Float)
    final_score = Column(Float)
    mood_class = Column(Text)
