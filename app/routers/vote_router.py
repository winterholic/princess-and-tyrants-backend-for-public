from fastapi import Request, APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.schemas.vote import Vote
from database_connect import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vote_dto import VoteReq
from sqlalchemy.future import select
from fastapi.security import APIKeyHeader
from app.services.vote_service import voteService

def verify_header(access_token=Security(APIKeyHeader(name='Authorization'))):
    return access_token

router = APIRouter()

@router.post("/vote", dependencies=[verify_header()], summary="투표 생성 api", description="", tags=["vote(투표)"])
async def create_vote(vote_req: VoteReq, request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)

    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await vote_service.create_vote(user.get("user_id"), vote_req.target_user_id, vote_req)
    return result

@router.get("/vote/result/my", dependencies=[verify_header()], summary="친구들이 생각하는 나의 mbti 결과 api", description="", tags=["vote(투표)"])
async def get_vote_my_result(request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)

    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await vote_service.get_vote_result(user.get("user_id"))
    return result

@router.get("/vote/list/my", dependencies=[verify_header()], summary="친구들이 생각하는 나의 mbti 방명록 api", description="", tags=["vote(투표)"])
async def get_vote_my_list(request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)

    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await vote_service.get_vote_list(user.get("user_id"))
    return result

@router.get("/home/vote/result/{user_id}", summary="친구들이 생각하는 나의 mbti 결과 api", description="", tags=["vote(투표)"])
async def get_vote_result(user_id: str, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)
    
    result = await vote_service.get_vote_result(user_id)
    return result

@router.get("/home/vote/list/{user_id}", summary="친구들이 생각하는 나의 mbti 방명록 api", description="", tags=["vote(투표)"])
async def get_vote_list(user_id: str,  db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)
    
    result = await vote_service.get_vote_list(user_id)
    return result