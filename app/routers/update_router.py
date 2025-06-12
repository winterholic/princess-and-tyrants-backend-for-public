from app.models.auth_dto import SignupReq, SigninReq
from sqlalchemy.ext.asyncio import AsyncSession
from database_connect import get_db
from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException, Security
from app.services.user_sevice import UserService
from app.models.user_dto import UpdateUserNicknameReq, UpdateUserMbtiReq
from fastapi.security import APIKeyHeader

def verify_header(access_token=Security(APIKeyHeader(name='Authorization'))):
    return access_token

router = APIRouter()

@router.patch("/user/update_nickname", dependencies=[verify_header()], summary="유저 닉네임 정보 업데이트", description="", tags=["유저 정보 Update"])
async def update_nickname(request: Request, update_user_nickname_req: UpdateUserNicknameReq, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await user_service.update_nickname(user.get("user_id"), update_user_nickname_req)
    return result

@router.patch("/user/update_mbti", dependencies=[verify_header()], summary="유저 mbti 정보 업데이트", description="", tags=["유저 정보 Update"])
async def update_mbti(request: Request, update_user_mbti_req: UpdateUserMbtiReq, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await user_service.update_mbti(user.get("user_id"), update_user_mbti_req)
    return result