import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.user import User
from app.schemas.cardcase import CardCase
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from sqlalchemy import and_, update
from sqlalchemy.exc import SQLAlchemyError
from app.models.auth_dto import SignupReq, SigninReq
from app.utils.aes_logic import key, iv, aes_decrypt
import bcrypt
from app.utils.jwt_token_generator import generate_jwt_token
from app.models.user_dto import UpdateUserNicknameReq, UpdateUserMbtiReq
from datetime import datetime


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_nickname(self, user_id : str, update_user_req: UpdateUserNicknameReq) :
        async with self.db.begin() as transaction:  # 트랜잭션 시작
            try:
                # 기존 사용자 검색
                query = select(User).where(and_(User.user_id == user_id, User.is_deleted == "N"))
                result = await self.db.execute(query)
                user = result.scalar_one_or_none()

                if not user:
                    raise HTTPException(status_code=450, detail="Resource not found")  # 450 : 해당 데이터 없음

                # 업데이트 쿼리 작성
                update_query = (
                    update(User)
                    .where(User.user_id == user_id)
                    .values(
                        nickname=update_user_req.nickname,
                        modified_date=datetime.now()  # 수정 날짜 갱신
                    )
                )

                # 업데이트 실행
                await self.db.execute(update_query)

                return {"message" : "닉네임이 성공적으로 업데이트되었습니다."}

            except HTTPException:
                # 특정 예외는 바로 전달
                raise
            except SQLAlchemyError as e:
                # SQLAlchemy 관련 에러 발생 시 롤백
                await transaction.rollback()
                raise HTTPException(status_code=400, detail="데이터베이스 에러") from e
    
        
    async def update_mbti(self, user_id : str, update_user_mbti: UpdateUserMbtiReq) :
        async with self.db.begin() as transaction:  # 트랜잭션 시작
            try:
                # 기존 사용자 검색
                query = select(User).where(and_(User.user_id == user_id, User.is_deleted == "N"))
                result = await self.db.execute(query)
                user = result.scalar_one_or_none()

                if not user:
                    raise HTTPException(status_code=450, detail="Resource not found")  # 450 : 해당 데이터 없음

                # 업데이트 쿼리 작성
                update_query = (
                    update(User)
                    .where(User.user_id == user_id)
                    .values(
                        mbti_ei_score = update_user_mbti.mbti_ei_score,
                        mbti_sn_score = update_user_mbti.mbti_sn_score,
                        mbti_tf_score = update_user_mbti.mbti_tf_score,
                        mbti_pj_score = update_user_mbti.mbti_pj_score,
                        modified_date=datetime.now()  # 수정 날짜 갱신
                    )
                )

                # 업데이트 실행
                await self.db.execute(update_query)

                return {"message" : "mbti가 성공적으로 업데이트되었습니다."}

            except HTTPException:
                # 특정 예외는 바로 전달
                raise
            except SQLAlchemyError as e:
                # SQLAlchemy 관련 에러 발생 시 롤백
                await transaction.rollback()
                raise HTTPException(status_code=400, detail="데이터베이스 에러") from e


    async def get_home_profile(self, user_id : str):
        query = select(User).where(and_(User.user_id == user_id, User.is_deleted == "N"))
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=450, detail="Resource not found") # 450 : 해당 데이터 
        
        mbti_first_element = 'I' if user.mbti_ei_score > 50 else 'E'
        mbti_second_element = 'N' if user.mbti_sn_score > 50 else 'S'
        mbti_third_element = 'F' if user.mbti_tf_score > 50 else 'T'
        mbti_forth_element = 'J' if user.mbti_pj_score > 50 else 'P'

        mbti = mbti_first_element + mbti_second_element + mbti_third_element + mbti_forth_element

        return {"userId" : user.user_id, "nickname" : user.nickname, "mbti" : mbti, "mbti_ei_score" : user.mbti_ei_score,
                "mbti_sn_score" : user.mbti_sn_score, "mbti_tf_score" : user.mbti_tf_score, "mbti_pj_score" : user.mbti_pj_score}


    async def check_duplicate_id(self, id : str):
        query = select(exists().where(and_(User.id == id, User.is_deleted == "N")))
        result = await self.db.execute(query)
        is_duplicate = result.scalar()

        if is_duplicate:
            raise HTTPException(status_code=400, detail="ID가 중복되었습니다.") # 400 : id가 중복된 경우
        
        return {"message": "사용가능한 ID입니다."} # 200 : id가 중복되지 않은 경우
    

    async def signup(self, signup_req: SignupReq):
        try:
            # NOTE : password 해시는 제거하기, HTTPS를 붙이면 됨
            # NOTE : 이전 코드
            # decrypted_password = aes_decrypt(signup_req.password, key, iv)
            # password_bytes = decrypted_password.encode('utf-8')
            # hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            # NOTE : 이전 코드

            password_bytes = signup_req.password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

            # UUID 자동 생성
            new_user = User(
                user_id=str(uuid.uuid4()),  # UUID 생성
                id=signup_req.id,  # UserReq에서 값 가져오기
                nickname=signup_req.nickname,
                password=hashed_password,  # 비밀번호는 해시 처리 필요
                mbti_ei_score=signup_req.mbti_ei_score,
                mbti_sn_score=signup_req.mbti_sn_score,
                mbti_tf_score=signup_req.mbti_tf_score,
                mbti_pj_score=signup_req.mbti_pj_score
            )

            # DB에 새 사용자 추가
            self.db.add(new_user)
            await self.db.commit()  # 트랜잭션 커밋
            return {"message": "User created successfully"}

        except Exception as e:
            await self.db.rollback()  # 에러 발생 시 롤백
            raise HTTPException(status_code=400, detail="회원가입에 실패하였습니다.")

        finally:
            await self.db.close()

    async def signin(self, signin_req: SigninReq):
        # NOTE : password 해시는 제거하기, HTTPS를 붙이면 됨
        # NOTE : 이전 코드
        # decrypted_password = aes_decrypt(signin_req.password, key, iv)
        query = select(User).where(and_(User.id == signin_req.id, User.is_deleted == "N"))
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=451, detail="아이디가 유효하지 않습니다.") # 451 : id가 유효하지 않은 경우
            
        # 비밀번호 검증
        if not bcrypt.checkpw(signin_req.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=452, detail="비밀번호가 유효하지 않습니다.") # 452 : pw가 유효하지 않은 경우

        await self.db.close()  # 세션 닫기
        return {"accessToken" : generate_jwt_token(user.user_id)}
    
    async def is_friend(self, this_user_id : str, target_user_id : str):
        # decrypted_password = aes_decrypt(signin_req.password, key, iv)
        query = select(CardCase).where(
            and_(
                CardCase.owner_user_id == this_user_id,
                CardCase.collected_user_id == target_user_id,
                CardCase.is_deleted == "N"
            )
        )
        result = await self.db.execute(query)
        card_case = result.scalar_one_or_none()
        if not card_case:
            return {"isFriend": False, "message" : "친구가 아닙니다."}
        
        return {"isFriend": True, "message" : "친구입니다."}