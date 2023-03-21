from fastapi import APIRouter, Response, Depends

from components.database import get_db
from components.user.models import (
    LoginIDChecker, RegisterUser, ModifiyUser,
    LoginUser, db_delete
)

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)

# 사용가능한 아이디 확인
@router.get("/{login_id}")
async def check_login_id_exsist(login_id: str, db = Depends(get_db)):
    await LoginIDChecker(login_id=login_id).is_possible_to_use(db)
    return Response(status_code=200)

# 등록
@router.post("/register")
async def sign_up_user(user: RegisterUser, db = Depends(get_db)):
    await user.db_insert(db)
    return Response(status_code=201)

# 로그인
@router.post("/login")
async def login(user: LoginUser, db = Depends(get_db)):
    return await user.is_valid_user(db)

## Auth 추가
# 유저 정보 수정
@router.put("/{user_id}")
async def update_user_info(user_id: int, user: ModifiyUser, db = Depends(get_db)):
    await user.db_update(user_id, db)
    return Response(status_code=201)

# 유저 삭제
@router.put("/{user_id}")
async def delete_user(user_id: int, db = Depends(get_db)):
    await db_delete(user_id, db)
    return Response(status_code=200)