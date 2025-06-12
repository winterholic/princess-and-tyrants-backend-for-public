import base64  # Base64 인코딩 및 디코딩을 위한 모듈
from Crypto.Cipher import AES  # AES 암호화를 위한 모듈
from Crypto.Util.Padding import pad, unpad  # 데이터 패딩 및 패딩 제거를 위한 모듈
from Crypto.Random import get_random_bytes  # 랜덤 바이트 생성을 위한 모듈
from fastapi import APIRouter, HTTPException


# AES 암호화에 사용할 랜덤 키 생성 (32바이트, AES-256용)
key = base64.b64decode("orgH1VGPj3ZfpdPanx/Rx1fDl1QCDDtFNx7ltYYF9f4=")  # 32바이트 길이의 랜덤 키
# AES CBC 모드에서 사용할 초기화 벡터(IV) 생성 (16바이트)
iv = base64.b64decode("NGK7TQcuvspBSMImohFPvA==")  # 16바이트 길이의 랜덤 IV

# 생성된 키와 IV를 Base64로 출력하여 확인
# print(f"KEY: {base64.b64encode(key).decode()}")  # Base64로 키를 인코딩하여 출력
# print(f"IV: {base64.b64encode(iv).decode()}")  # Base64로 IV를 인코딩하여 출력


router = APIRouter()

@router.get("/generate_key")
def generate_random_secret_key(length: int):
    # 랜덤 바이트 생성
    random_bytes = get_random_bytes(length)
    # base64로 인코딩하여 문자열로 반환
    return {"secret_key": base64.b64encode(random_bytes).decode('utf-8')}


@router.get("/generate_key_base64")
def generate_random_secret_key_base64(key) :
    return {"secret_key": base64.b64encode(base64.b64encode(key).decode()).decode('utf-8')}



# AES 암호화를 수행하는 함수
@router.get("/make_test_password")
def aes_encrypt(data, key, iv):
    """
    주어진 데이터를 AES-256으로 암호화하고 Base64로 인코딩합니다.
    :param data: 암호화할 문자열 데이터
    :param key: AES-256 암호화에 사용할 키 (32바이트)
    :param iv: 초기화 벡터 (16바이트)
    :return: Base64로 인코딩된 암호화된 문자열
    """
    key = base64.b64decode("orgH1VGPj3ZfpdPanx/Rx1fDl1QCDDtFNx7ltYYF9f4=")
    iv = base64.b64decode("NGK7TQcuvspBSMImohFPvA==")
    cipher = AES.new(key, AES.MODE_CBC, iv)  # AES CBC 모드로 암호화 객체 생성
    padded_data = pad(data.encode(), AES.block_size)  # 데이터를 AES 블록 크기(16바이트)에 맞게 패딩 처리
    encrypted = cipher.encrypt(padded_data)  # 패딩된 데이터를 암호화
    return base64.b64encode(encrypted).decode()  # 암호화된 데이터를 Base64로 인코딩하여 문자열로 반환

def aes_decrypt(encoded_data, key, iv):
    """
    Base64로 인코딩된 AES-256 암호화 데이터를 복호화합니다.
    :param encoded_data: Base64로 인코딩된 암호화된 데이터
    :param key: AES-256 암호화에 사용된 키 (32바이트)
    :param iv: 초기화 벡터 (16바이트)
    :return: 복호화된 원래 문자열 데이터
    """
    try:
        # AES 복호화 객체 생성
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Base64 디코딩
        encrypted_data = base64.b64decode(encoded_data)
        
        # 복호화 및 패딩 제거
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        # 문자열로 반환
        return decrypted.decode()
    
    except (ValueError, KeyError) as e:
        # 복호화 오류 처리
        raise HTTPException(status_code=452, detail="Password is invalid") # 452 : pw가 유효하지 않은 경우
    
    except Exception as e:
        # 기타 예상하지 못한 예외 처리
        raise HTTPException(status_code=452, detail="Password is invalid") # 452 : pw가 유효하지 않은 경우


# 암호화할 원본 데이터 정의
data = "Hello, AES-256 with Base64!"  # 암호화할 문자열 데이터

# 데이터 암호화 수행
encrypted = aes_encrypt(data, key, iv)  # AES 암호화 및 Base64 인코딩
# print(f"Encrypted (Base64): {encrypted}")  # 암호화된 데이터를 출력

# 데이터 복호화 수행
decrypted = aes_decrypt(encrypted, key, iv)  # Base64 디코딩 및 AES 복호화
# print(f"Decrypted: {decrypted}")  # 복호화된 원본 데이터를 출력
