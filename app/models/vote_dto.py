from pydantic import BaseModel

class VoteReq(BaseModel):
  target_user_id: str
  first_mbti_element: str
  second_mbti_element: str
  third_mbti_element: str
  forth_mbti_element: str
  comment: str | None = None
  incognito: str