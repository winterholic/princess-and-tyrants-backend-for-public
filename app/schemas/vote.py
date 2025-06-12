from sqlalchemy import Column, String, DateTime, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vote(Base):
    __tablename__ = "vote"

    vote_id = Column(String(50), primary_key=True, index=True, nullable=False, comment='투표 고유 ID (PK)')
    link_id = Column(String(50), nullable=False, comment='징검다리 테이블(vote_link)의 ID (FK)')
    voting_user_id = Column(String(50), nullable=False, comment='투표를 한 유저 ID (user 테이블의 user_id를 참조)')
    first_mbti_element = Column(String(1), nullable=False, comment='MBTI 첫 번째 요소 (E/I)')
    second_mbti_element = Column(String(1), nullable=False, comment='MBTI 두 번째 요소 (S/N)')
    third_mbti_element = Column(String(1), nullable=False, comment='MBTI 세 번째 요소 (T/F)')
    forth_mbti_element = Column(String(1), nullable=False, comment='MBTI 네 번째 요소 (P/J)')
    comment = Column(Text, nullable=True, comment='투표 관련 코멘트')  # TEXT로 수정
    incognito = Column(String(1), nullable=False, comment='가명')
    created_date = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='생성일')  # 기본값 수정
    modified_date = Column(DateTime, nullable=True, server_onupdate=func.current_timestamp(), comment='수정일')  # onupdate 수정
    is_deleted = Column(String(1), nullable=False, server_default='N', comment="삭제 여부 ('N': 활성, 'Y': 삭제됨)")
