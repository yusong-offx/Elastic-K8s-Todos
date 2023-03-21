import uvicorn
from main import app

# 중단점 설정후 디버깅 실행
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)