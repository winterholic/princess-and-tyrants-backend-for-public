from pydantic import BaseModel

class UpdateUserNicknameReq(BaseModel):
    nickname: str
    
class UpdateUserMbtiReq(BaseModel):
    mbti_ei_score : int
    mbti_sn_score : int
    mbti_tf_score : int
    mbti_pj_score : int