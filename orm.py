from sqlalchemy import Column, Integer, Float, Text, DateTime, Boolean, Index, CheckConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class MoodEntryORM(Base):
    """Pillar: Engine - The Core Clinical Data Store"""
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Text, nullable=False, index=True) # Indexed for O(1) lookups
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    # Flattened Q1-Q10 with Check Constraints for clinical validity (0-3 scale)
    q1 = Column(Integer, CheckConstraint('q1 >= 0 AND q1 <= 3'))
    q2 = Column(Integer, CheckConstraint('q2 >= 0 AND q2 <= 3'))
    q3 = Column(Integer, CheckConstraint('q3 >= 0 AND q3 <= 3'))
    q4 = Column(Integer, CheckConstraint('q4 >= 0 AND q4 <= 3'))
    q5 = Column(Integer, CheckConstraint('q5 >= 0 AND q5 <= 3'))
    q6 = Column(Integer, CheckConstraint('q6 >= 0 AND q6 <= 3'))
    q7 = Column(Integer, CheckConstraint('q7 >= 0 AND q7 <= 3'))
    q8 = Column(Integer, CheckConstraint('q8 >= 0 AND q8 <= 3'))
    q9 = Column(Integer, CheckConstraint('q9 >= 0 AND q9 <= 3')) # Suicidal Ideation Key
    q10 = Column(Integer) # Contextual or functional impairment question

    fill_word = Column(Text)
    
    # Scoring & Velocity Analytics
    raw_score = Column(Integer)
    weighted_score = Column(Float)
    final_score = Column(Float, index=True) # Indexed for rapid triage sorting
    mood_class = Column(Text)
    
    # Pillar: Care - Immediate Flags
    is_crisis = Column(Boolean, default=False, index=True)
    velocity_alert = Column(Boolean, default=False) # True if score drop is > threshold

    # Metadata for the Adaptive Pillar
    intervention_delivered = Column(Text) # Record of which resource.json tool was shown

class AuditLogORM(Base):
    """Pillar: Engine - HIPAA Accountability Layer"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    clinician_id = Column(Text, nullable=False, index=True)
    target_user_id = Column(Text, nullable=False)
    action_type = Column(Text, nullable=False) # e.g., 'VIEW_TRIAGE', 'RESOLVE_CRISIS'
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ip_address = Column(Text)

# High-Performance Composite Indices
# Allows the dashboard to instantly fetch a specific user's history ordered by time
Index('idx_user_timestamp', MoodEntryORM.user_id, MoodEntryORM.timestamp.desc())
