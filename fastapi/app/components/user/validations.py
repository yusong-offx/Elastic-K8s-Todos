import re
import bcrypt


# 비밀번호 유효성 검사 정규표현식
# 최소 1개 이상의 영단어, 1개 이상의 숫자, 1개 이상의 특수문자, 8-20자 사이
is_password_validation = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$")

# Login_id는 20자 이하
def login_id_must_max_20(v):
    if not (len(v) <= 20):
        raise ValueError("login_id must not be longer than 20 characters")
    return v

# 가입시 패스워드는 위 정규표현식을 통해 검사
def password_must_validate(v):
    if not is_password_validation.match(v):
        raise ValueError("password must include at least 1 char, 1 number, 1 special and min 8, max 20")
    return v

def is_login_id_exsist(conn, login_id: str) -> tuple|None:
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM users WHERE login_id = %s",
            (login_id,)
        )
        return cursor.fetchone()
    
def bcrypt_hashing(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

def is_user_password(input_pwd: str, cmp: str) -> bool:
    return bcrypt.checkpw(input_pwd.encode("utf-8"), cmp.encode("utf-8"))