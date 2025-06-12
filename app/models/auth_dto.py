from pydantic import BaseModel

class SignupReq(BaseModel):
    id: str
    nickname: str
    password : str
    mbti_ei_score : int
    mbti_sn_score : int
    mbti_tf_score : int
    mbti_pj_score : int

class SigninReq(BaseModel):
    id : str
    password : str