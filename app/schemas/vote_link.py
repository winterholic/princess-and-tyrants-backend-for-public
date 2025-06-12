from sqlalchemy import Column, String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class VoteLink(Base):
    __tablename__ = "vote_link"

    link_id = Column(String(50), primary_key=True, index=True, comment="UUID (PK)")
    target_user_id = Column(String(50), nullable=False, comment="투표 대상 유저 ID (user 테이블 참조)")
    created_date = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='생성일')  # 기본값 수정
    modified_date = Column(DateTime, nullable=True, server_onupdate=func.current_timestamp(), comment='수정일')
    is_deleted = Column(String(1), nullable=False, default="N", comment="삭제 여부 ('N': 활성, 'Y': 삭제됨)")

    __table_args__ = (
        UniqueConstraint('target_user_id', name='vote_link_unique'),
    )