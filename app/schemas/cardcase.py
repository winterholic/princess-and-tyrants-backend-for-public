from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CardCase(Base):
    __tablename__ = "cardcase"

    # Columns
    cardcase_id = Column(String(50), primary_key=True, comment="Primary Key (UUID)")
    owner_user_id = Column(String(50), nullable=False, comment="명함 보관자 (Owner)")
    collected_user_id = Column(String(50), nullable=False, comment="명함 소유자 (Collected)")
    created_date = Column(DateTime, nullable=False, server_default=func.now(), comment="생성일")
    modified_date = Column(DateTime, nullable=True, onupdate=func.now(), comment="수정일")
    is_deleted = Column(VARCHAR(1), nullable=False, default="N", comment="삭제 여부 ('N': 활성, 'Y': 삭제됨)")

    def __repr__(self):
        return (
            f"<CardCase(cardcase_id='{self.cardcase_id}', "
            f"owner_user_id='{self.owner_user_id}', "
            f"collected_user_id='{self.collected_user_id}', "
            f"is_deleted='{self.is_deleted}')>"
        )