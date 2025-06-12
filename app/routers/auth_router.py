from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException
from app.services.user_sevice import UserService
from app.models.auth_dto import SignupReq, SigninReq
from sqlalchemy.ext.asyncio import AsyncSession
from database_connect import get_db

router = APIRouter()

@router.post("/signup", summary="회원가입 api", description="별도의 예외처리는 X, 에러발생시 400 or 404 혹은 500", tags=["Auth"])
async def signup(signup_req: SignupReq, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    result = await user_service.signup(signup_req)
    return result
    
@router.post("/check/id", summary="닉네임 중복검사 api", description="예외처리시 404", tags=["Auth"])
async def check_duplicate_id(id : str, db: AsyncSession = Depends(get_db)) :
    user_service = UserService(db)
    result = await user_service.check_duplicate_id(id)
    return result
    
@router.post("/signin", summary="로그인 api", description="id없을시 451, pw일치하지 않을 시 452, 그 이외의 에러는 400 or 404 혹은 500", tags=["Auth"])
async def signin(signin_req: SigninReq, db: AsyncSession = Depends(get_db)) :
    user_service = UserService(db)
    result = await user_service.signin(signin_req)
    return result