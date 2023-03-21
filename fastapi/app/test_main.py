
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 사용가능한 아이디
def test_login_id_check():
    response = client.get(
        "/user/hello"
    )
    assert response.status_code == 200

# 20자가 넘는 유저 아이디
def test_user_login_id_over_20char():
    response = client.get(
        "/user/hellohellohellohellohello"
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "login_id must not be longer than 20 characters"

# 잘못된 가입
def test_user_sign_up():
    # 비밀번호 오류
    response = client.post(
            "/user/register", 
            json={
                "login_id" : "hello",
                "login_password" : "world123",
                "first_name" : "yujin",
                "last_name" : "song",
                "email" : "example@good.com"
            }
        )
    assert response.status_code == 422

    # 아이디
    response = client.post(
            "/user/register", 
            json={
                "login_id" : "hellohellohellohello1",
                "login_password" : "world123!",
                "first_name" : "yujin",
                "last_name" : "song",
                "email" : "example@good.com"
            }
        )
    assert response.status_code == 422

# 가입
def test_user_sign_up():
    response = client.post(
            "/user/register", 
            json={
                "login_id" : "hello",
                "login_password" : "world123!",
                "first_name" : "yujin",
                "last_name" : "song",
                "email" : "example@good.com"
            }
        )
    assert response.status_code == 201

# 중복된 유저 아이디
def test_user_login_id_already_exsist():
    response = client.get(
        "/user/hello"
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "ID already exsists"
    
# 로그인 실패
def test_user_login():
    # login_id 실패
    response = client.post(
            "/user/register", 
            json={
                "login_id" : "hello1",
                "login_password" : "world123!",
            }
        )
    assert response.status_code == 401
    
    # login_password 실패
    response = client.post(
            "/user/register", 
            json={
                "login_id" : "hello",
                "login_password" : "world123!1",
            }
        )
    assert response.status_code == 401

# 수정 
def user_info_modify(user_data: dict):
    id = user_data["id"]
    response = client.put(
            f"/user/{id}", 
            json={
                "login_id" : "hello1",
                "login_password" : "world123!1",
                "first_name" : "yujin1",
                "last_name" : "song1",
                "email" : "example@good.com1"
            }
        )
    assert response.status_code == 201

# 로그인
def test_user_login():
    response = client.post(
            "/user/login", 
            json={
                "login_id" : "hello",
                "login_password" : "world123!",
            }
        )
    body = response.json()
    assert response.status_code == 200
    assert body["login_id"] == "hello"
    assert body["first_name"] == "yujin"
    assert body["last_name"] == "song"
    assert body["email"] == "example@good.com"

    user_info_modify(body)
    response = client.post(
        "/user/login", 
        json={
            "login_id" : "hello1",
            "login_password" : "world123!1",
        }
    )
    body = response.json()
    assert response.status_code == 200
    assert body["login_id"] == "hello1"
    assert body["first_name"] == "yujin1"
    assert body["last_name"] == "song1"
    assert body["email"] == "example@good.com1"
    
