from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import declarative_base
from datetime import datetime
from database_connect import Base
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(String(50), primary_key=True, index=True, comment="UUID")
    id = Column(String(50), unique=True, nullable=False, comment="사용자 ID, 고유 값")
    mbti_ei_score = Column(Integer, nullable=False, comment="MBTI 첫 번째 요소 (E,I) 점수")
    mbti_sn_score = Column(Integer, nullable=False, comment="MBTI 두 번째 요소 (S,N) 점수")
    mbti_tf_score = Column(Integer, nullable=False, comment="MBTI 세 번째 요소 (T,F) 점수")
    mbti_pj_score = Column(Integer, nullable=False, comment="MBTI 네 번째 요소 (P,J) 점수")
    nickname = Column(String(50), nullable=False, comment="닉네임")
    password = Column(String(255), nullable=False, comment="비밀번호 (암호화된 해시 사용)")
    created_date = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='생성일')  # 기본값 수정
    modified_date = Column(DateTime, nullable=True, server_onupdate=func.current_timestamp(), comment='수정일')
    is_deleted = Column(String(1), nullable=False, default="N", comment="삭제 여부 ('N': 활성, 'Y': 삭제됨)")