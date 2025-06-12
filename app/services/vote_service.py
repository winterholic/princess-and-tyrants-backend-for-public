import uuid
import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.vote_dto import VoteReq
from app.schemas.user import User
from app.schemas.vote import Vote
from app.schemas.vote_link import VoteLink
from sqlalchemy import func, and_

class voteService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_vote(self, voting_user_id: str, voted_user_id: str, VoteReq: VoteReq):
        try:
            # VoteLink 객체 조회 또는 생성
            query = select(VoteLink).where(VoteLink.target_user_id == voted_user_id)
            result = await self.db.execute(query)
            new_vote_link = result.scalars().first()

            if new_vote_link is None:
                new_vote_link = VoteLink(
                    link_id=str(uuid.uuid4()),
                    target_user_id=voted_user_id
                )
                self.db.add(new_vote_link)
                await self.db.commit()
                await self.db.refresh(new_vote_link)
            
            query = select(Vote).where(
                and_(
                    Vote.voting_user_id == voting_user_id,
                    Vote.link_id == new_vote_link.link_id
                )
            )
            result = await self.db.execute(query)
            existing_vote = result.scalars().first()  # 또는 .one_or_none()
            if existing_vote:
                raise HTTPException(status_code=470, detail="이미 존재하는 투표입니다.")
                        

            new_vote = Vote(
                vote_id=str(uuid.uuid4()),  # UUID 생성
                voting_user_id=voting_user_id,
                link_id=new_vote_link.link_id,
                first_mbti_element=VoteReq.first_mbti_element,
                second_mbti_element=VoteReq.second_mbti_element,
                third_mbti_element=VoteReq.third_mbti_element,
                forth_mbti_element=VoteReq.forth_mbti_element,
                comment=VoteReq.comment,
                incognito=VoteReq.incognito
            )
            self.db.add(new_vote)  # 세션에 추가
            await self.db.commit()  # 트랜잭션 커밋
            await self.db.refresh(new_vote)  # 새로 생성된 Vote 객체를 갱신
            # 성공적인 삽입 후 반환 데이터 구성
            
            # 성공적인 삽입 후 반환 데이터 구성
            return {
                "message": "success",
                "data": {
                    "vote_id": new_vote.vote_id
                }
            }
        
        except HTTPException as http_exc:
            await self.db.rollback()
            raise http_exc
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="투표 결과 데이터 생성중에 오류가 발생했습니다. 다시 시도해주세요.")
    
    async def get_vote_result(self, user_id : str):
        # VoteLink 객체 조회
        query = select(VoteLink).where(VoteLink.target_user_id == user_id)
        result = await self.db.execute(query)
        user_vote_link = result.scalars().first()

        if user_vote_link is None:
            user_vote_link = VoteLink(
                link_id=str(uuid.uuid4()),
                target_user_id=user_id,
                is_deleted="N"
            )
            self.db.add(user_vote_link)
            await self.db.commit()
            await self.db.refresh(user_vote_link)

        query = select(Vote).where(Vote.link_id == user_vote_link.link_id, Vote.is_deleted == "N")
        result = await self.db.execute(query)
        user_vote = result.scalars().all()

        mbti_ei_score = 0
        mbti_sn_score = 0
        mbti_tf_score = 0
        mbti_jp_score = 0
        mbti_result = None

        mbti_i_count = 0
        mbti_n_count = 0
        mbti_f_count = 0
        mbti_p_count = 0

        total_count = 0

        for vote in user_vote:
            total_count += 1

            if vote.first_mbti_element == "I":
                mbti_i_count += 1
            if vote.second_mbti_element == "N":
                mbti_n_count += 1
            if vote.third_mbti_element == "F":
                mbti_f_count += 1
            if vote.forth_mbti_element == "P":
                mbti_p_count += 1
            
        # MBTI 점수 계산
        if total_count > 0:
            mbti_ei_score = (mbti_i_count / total_count) * 100
            mbti_sn_score = (mbti_n_count / total_count) * 100
            mbti_tf_score = (mbti_f_count / total_count) * 100
            mbti_jp_score = (mbti_p_count / total_count) * 100

            mbti_result = ""
            mbti_result += "E" if mbti_ei_score < 50 else "I"
            mbti_result += "S" if mbti_sn_score < 50 else "N"
            mbti_result += "T" if mbti_tf_score < 50 else "F"
            mbti_result += "J" if mbti_jp_score < 50 else "P"
        else:
            mbti_result = None
        

        # 성공적인 삽입 후 반환 데이터 구성
        return {
            "message": "cardcase created successfully",
            "data": {
                "total_count": total_count,
                "mbti_ei_score": mbti_ei_score,
                "mbti_sn_score": mbti_sn_score,
                "mbti_tf_score": mbti_tf_score,
                "mbti_jp_score": mbti_jp_score,
                "mbti_result": mbti_result
            }
        }
    
    async def get_vote_list(self, user_id : str):
        # VoteLink 객체 조회
        query = select(VoteLink).where(VoteLink.target_user_id == user_id)
        result = await self.db.execute(query)
        user_vote_link = result.scalars().first()

        if user_vote_link is None:
            user_vote_link = VoteLink(
                link_id=str(uuid.uuid4()),
                target_user_id=user_id,
                is_deleted="N"
            )
            self.db.add(user_vote_link)
            await self.db.commit()
            await self.db.refresh(user_vote_link)

        query = select(Vote).where(
            Vote.link_id == user_vote_link.link_id,
            Vote.is_deleted == "N"
        ).order_by(Vote.created_date.desc())
        result = await self.db.execute(query)
        user_vote = result.scalars().all()

        # voting_user_id를 기준으로 유저 정보 조회 및 딕셔너리 생성
        voting_user_ids = list(set([vote.voting_user_id for vote in user_vote]))

        query = select(User).where(User.user_id.in_(voting_user_ids), User.is_deleted == "N")
        result = await self.db.execute(query)
        users = result.scalars().all()
        user_nickname_dict = {user.user_id: user.nickname for user in users}
        user_mbti_dict = {}
        for user in users:
            mbti_result = ""
            mbti_result += "E" if user.mbti_ei_score < 50 else "I"
            mbti_result += "S" if user.mbti_sn_score < 50 else "N"
            mbti_result += "T" if user.mbti_tf_score < 50 else "F"
            mbti_result += "J" if user.mbti_pj_score < 50 else "P"
            user_mbti_dict[user.user_id] = mbti_result

        result_list = []
        
        for vote in user_vote:
            mbti_result = ""
            mbti_result += vote.first_mbti_element
            mbti_result += vote.second_mbti_element
            mbti_result += vote.third_mbti_element
            mbti_result += vote.forth_mbti_element

            voting_user_nickname = "익명"
            if vote.incognito == "N":
                voting_user_nickname = user_nickname_dict.get(vote.voting_user_id, "Unknown")

            user_vote_dict = {
                "vote_id": vote.vote_id,
                "voting_user_id": vote.voting_user_id,
                "voting_user_nickname": voting_user_nickname,
                "voting_user_mbti": user_mbti_dict.get(vote.voting_user_id, "Unknown"),
                "mbti_result": mbti_result,
                "comment": vote.comment,
                "incognito": vote.incognito
            }
            result_list.append(user_vote_dict)

        # 성공적인 삽입 후 반환 데이터 구성
        return {
            "message": "success",
            "data": result_list
        }