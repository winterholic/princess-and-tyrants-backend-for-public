from app.models.auth_dto import SignupReq, SigninReq
from sqlalchemy.ext.asyncio import AsyncSession
from database_connect import get_db
from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException, Security
from app.services.user_sevice import UserService
from fastapi.security import APIKeyHeader

def verify_header(access_token=Security(APIKeyHeader(name='Authorization'))):
    return access_token

router = APIRouter()

@router.get("/home/profile", summary="유저 기본 정보 조회 api", description="", tags=["Home"])
async def get_home_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    
    result = await user_service.get_home_profile(user_id)
    return result

@router.get("/my/home/profile", dependencies=[verify_header()], summary="유저 본인 기본 정보 조회 api", description="", tags=["Home"])
async def get_home_my_profile(request: Request, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await user_service.get_home_profile(user.get("user_id"))
    return result

@router.get("/my/home/profile/friends", dependencies=[verify_header()], summary="유저가 친구인지 조회하는 api", description="", tags=["Home"])
async def get_is_friends(request: Request, user_id: str, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await user_service.is_friend(user.get("user_id"), user_id)
    return result