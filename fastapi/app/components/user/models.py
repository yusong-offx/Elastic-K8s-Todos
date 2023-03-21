from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, validator

from .validations import (
    login_id_must_max_20, 
    password_must_validate,
    is_login_id_exsist,
    bcrypt_hashing,
    is_user_password
)

# Login_id 중복 검사
class LoginIDChecker(BaseModel):
    login_id: str

    ###
    # 데이터 베이스
    async def is_possible_to_use(self, conn):
        is_exsist = None
        try:
            # Login_id 유효성 검사
            login_id_must_max_20(self.login_id)

            # DB에서 중복 검사
            is_exsist = is_login_id_exsist(conn, self.login_id)
        except ValueError as e: # Validation error
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e: # DB error
            raise HTTPException(status_code=500, detail=str(e))
        if is_exsist: # Login_id가 사용중(존재)
            raise HTTPException(status_code=422, detail="ID already exsists")

# 가입시 유저 데이터
class RegisterUser(BaseModel):
    login_id: str
    login_password: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

    ###
    # 유효성 검증
    _id_checker = validator("login_id", allow_reuse=True)(login_id_must_max_20)
    _pwd_checker = validator("login_password", allow_reuse=True)(password_must_validate)

    ###
    # 데이터 베이스
    async def db_insert(self, conn):
        try:
            # 비밀번호 해싱(bcrypt)
            hash_pwd = bcrypt_hashing(self.login_password)

            # 데이터 베이스 저장
            with conn.cursor() as cursor:
                now = datetime.now()
                cursor.execute(
                    """
                    INSERT INTO users ( 
                        login_id, 
                        login_password, 
                        first_name, 
                        last_name, 
                        email, 
                        last_login_at, 
                        join_at 
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        self.login_id,
                        hash_pwd,
                        self.first_name,
                        self.last_name,
                        self.email,
                        now,
                        now
                    )
                )
                conn.commit()
        except Exception as e: # DB 또는 Bcrypt error
            raise HTTPException(status_code=500, detail=str(e))

# 수정시 유저 데이터
class ModifiyUser(BaseModel):
    login_id: str
    login_password: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

    ###
    # 유효성 검증
    _id_checker = validator("login_id", allow_reuse=True)(login_id_must_max_20)
    _pwd_checker = validator("login_password", allow_reuse=True)(password_must_validate)

    ###
    # 데이터 베이스
    async def db_update(self, user_id, conn):
        try:
            # 비밀번호 해싱(bcrypt)
            self.login_password = bcrypt_hashing(self.login_password)

            # jwt user
            user_id = user_id
            
            # 데이터 베이스 저장
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        UPDATE users SET 
                        login_id=%s, 
                        login_password=%s, 
                        first_name=%s, 
                        last_name=%s, 
                        email=%s
                        WHERE
                        id = %s
                    """,
                    (
                        self.login_id,
                        self.login_password,
                        self.first_name,
                        self.last_name,
                        self.email,
                        user_id
                    )
                )
                conn.commit()
        except Exception as e: # DB 또는 Bcrypt error
            raise HTTPException(status_code=500, detail=str(e))

# 로그인 성공후 return body 
class ResponseUser(BaseModel):
    id: int
    login_id: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    last_login_at: datetime
    join_at: datetime

# 로그인시 get body
class LoginUser(BaseModel):
    login_id: str
    login_password: str
    
    # Login_id validation 검사
    _id_check = validator("login_id", allow_reuse=True)(login_id_must_max_20)

    async def is_valid_user(self, conn):
        try:
            with conn.cursor() as cursor:
                # 로그인 정보확인
                cursor.execute(
                    """
                    SELECT * FROM users
                    WHERE login_id = %s
                    """,
                    (self.login_id,)
                )
                user = cursor.fetchone()
                
                # 로그인 성공
                if user and is_user_password(self.login_password, user[2]):
                    last_login_at = datetime.now()
                    cursor.execute(
                        """
                            UPDATE users SET
                            last_login_at=%s
                            WHERE
                            login_id=%s
                        """,
                        (
                            last_login_at,
                            self.login_id
                        )
                    )
                    conn.commit()
                    return ResponseUser(
                        id=user[0],
                        login_id=user[1],
                        first_name=user[3],
                        last_name=user[4],
                        email=user[5],
                        last_login_at=last_login_at,
                        join_at=user[7]
                    )
                # 로그인 실패
                raise ValueError("check login_id or login_password")
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
        except Exception as e: # DB error
            raise HTTPException(status_code=500, detail=str(e))
        
async def db_delete(user_id: int, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM users
                WHERE id = %s
                """,
                (
                    user_id,
                )
            )
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))