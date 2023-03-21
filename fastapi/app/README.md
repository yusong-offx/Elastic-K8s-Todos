# By FastAPI
## 이 코드의 특징
- 추상화된 멀티쓰레드 데이터베이스 커넥션 풀 사용.
- 테스트 코드작성
- 요일 char(1)로 저장, index 설정
- FastAPI는 자동으로 Swagger를 생성해줍니다. (/docs 또는 /redoc)
- CORS 적용
- 요일 저장시 Postgresql Enum 사용시 4bytes를 차지하기 때문에 수동으로 변환

- JWT 적용

## 테스트
DB CRUD를 사용하기 때문에 연결되어 있는 postgresql을 실행 시켜야합니다.   
pytest 설치후 실행