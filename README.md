# Assignment4

원티드x위코드 백엔드 프리온보딩 과제4
- 과제 출제 기업 정보
  - 기업명 : 8퍼센트
  -  [8퍼센트 사이트](https://8percent.kr/)
  - [원티드 채용 링크](https://www.wanted.co.kr/wd/64695)

## Members
|이름   |github                   |담당 기능|
|-------|-------------------------|--------------------|
|김태우 |[jotasic](https://github.com/jotasic)       | API(거래내역)                           |
|고유영 |[lunayyko](https://github.com/lunayyko)     | API(회원가입, 로그인, 로그아웃), 배포환경설정  |
|박지원 |[jiwon5304](https://github.com/jiwon5304)   | API(회원가입, 로그인, 로그아웃)             |
|최신혁 |[shchoi94](https://github.com/shchoi94)     | API(계좌생성, 계좌목록조회, 입금, 출금), swagger 세팅|
|박세원 |[sw-develop](https://github.com/sw-develop) | API(거래내역), Functional Test         |

## 과제 내용

### [필수 포함 사항]

- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

> 📝 “계좌 거래 API”를 구현해주세요. API는 3가지가 구현되어야 합니다.


 **✔️ API 목록**
---
- 거래내역 조회 API
- 입금 API
- 출금 API

**✔️ 주요 고려 사항은 다음과 같습니다.**
---
- 계좌의 잔액을 별도로 관리해야 하며, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장
- DB를 설계 할때 각 칼럼의 타입과 제약

**✔️ 구현하지 않아도 되는 부분은 다음과 같습니다.**
---
- 문제와 관련되지 않은 부가적인 정보. 예를 들어 사용자 테이블의 이메일, 주소, 성별 등
- 프론트앤드 관련 부분

**✔️  제약사항은 다음과 같습니다.**
---
- (**8퍼센트가 직접 로컬에서 실행하여 테스트를 원하는 경우를 위해**) 테스트의 편의성을 위해 mysql, postgresql 대신 sqllite를 사용해 주세요.

**✔️  상세설명**
---
**1)** 거래내역 조회 **API**

- 아래와 같은 조회 화면에서 사용되는 API를 고려하시면 됩니다.
    

거래내역 API는 다음을 만족해야 합니다.
- 계좌의 소유주만 요청 할 수 있어야 합니다.
- 거래일시에 대한 필터링이 가능해야 합니다.
- 출금, 입금만 선택해서 필터링을 할 수 있어야 합니다.
- Pagination이 필요 합니다.
- 다음 사항이 응답에 포함되어야 합니다.
    - 거래일시
    - 거래금액
    - 잔액
    - 거래종류 (출금/입금)
    - 적요

**2)** 입금 **API**

입금 API는 다음을 만족해야 합니다.
- 계좌의 소유주만 요청 할 수 있어야 합니다.

**3)** 출금 **API**
출금 API는 다음을 만족해야 합니다.
- 계좌의 소유주만 요청 할 수 있어야 합니다.
- 계좌의 잔액내에서만 출금 할 수 있어야 합니다. 잔액을 넘어선 출금 요청에 대해서는 적절한 에러처리가 되어야 합니다.

**4)** 가산점
다음의 경우 가산점이 있습니다.
- Unit test의 구현
- Functional Test 의 구현 (입금, 조회, 출금에 대한 시나리오 테스트)
- 거래내역이 1억건을 넘어갈 때에 대한 고려
    - 이를 고려하여 어떤 설계를 추가하셨는지를 README에 남겨 주세요.

## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/sqlite-0064a5?style=for-the-badge&logo=sqlite&logoColor=white"/>&nbsp;
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/SWAGGER-5B8C04?style=for-the-badge&logo=Swagger&logoColor=white"/>&nbsp;

## 모델링
---
![image](https://user-images.githubusercontent.com/8219812/141481348-01525848-e996-4477-9b1f-e1a63ed016a2.png)


## API
---
[링크-Swagger](http://18.188.189.173:8031/swagger/)

## 구현 기능
---
1. 회원가입, 로그인, 로그아웃
- 커스텀 유저모델 생성, username 대신 email을 사용
- rest_auth 사용, 로그인 시 토큰 생성
2. 입급, 출금 API
- 계좌의 소유주만 계좌에서 입금, 출금 
- 잔액을 넘어서 출금 요청을 하면 에러 메세지 반환
3. 거래 내역 조회 API
- 계좌의 소유주만 거래 내역 조회 가능
- 입금, 출금만 선택해서 필터링
- 거래일시별로 조회기간을 정해서 필터링 
- Pagination

## 거래내역이 1억건을 넘어갈 때에 대한 고려
### sqlite 설정
```python
from django.db.backends.signals import connection_created


def activate_db_optimize(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA synchronous = OFF;')
        cursor.execute('PRAGMA journal_mode = MEMORY;')
        cursor.execute('PRAGMA cache_size = 10000;')
        cursor.execute('PRAGMA temp_store = MEMORY;')
        

connection_created.connect(activate_db_optimize)
```

## 배포정보
---
|구분   |  정보          |비고|
|-------|----------------|----|
|배포플랫폼 | AWS EC2    |    |
|API 주소 | http://18.188.189.173:8031/            |    |


## API TEST 방법
1. 우측 링크를 클릭해서 postman으로 들어갑니다. [링크](https://www.postman.com/wecode-21-1st-kaka0/workspace/assignment4)

2. 정의된 SERVER_URL이 올바른지 확인 합니다. (18.188.189.173:8031)


3. 만약 Send버튼이 비활성화가 될 시 fork를 이용해서 해당 postman project를 복사해서 시도하길 바랍니다.
![image](https://user-images.githubusercontent.com/8219812/139912241-d6cb5831-23e8-4cbb-a747-f52c42601098.png)


## 설치 및 실행 방법
###  Local 개발 및 테스트용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment4
    cd Assignment4
    ```

2. 가상 환경을 만들고 프로젝트에 사용한 python package를 받는다.
    ```bash
    conda create --name Assignment4 python=3.8
    conda actvate Assignment4
    pip install -r requirements.txt
    ```

3. Django SECRET_KEY용 환경 변수를 등록한다.
   ```bash
      export DJANGO_SECRET_KEY='django시크릿키'
    ```

4. db를 table 구조를 최신 model에 맞게 설정한다.
    ```bash
    python manage.py migrate
    ```

5. 서버를 실행한다.
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

###  배포용 
1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment4
    cd Assignment4
    ```

2. docker환경 설정 파일을 만든다.

  
3. 백엔드 서버용 .dockerenv.deploy.backend 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
    ### .dockerenv.deploy.backend
    ```text
      DJANGO_SECRET_KEY='django시크릿키'
    ```
       
4. docker-compose를 통해서 db와 서버를 실행시킨다.
    
    ```bash
    docker-compose -f docker-compose-deploy.yml up
    ```
    
5. 만약 백그라운드에서 실행하고 싶을 시 `-d` 옵션을 추가한다.
  
    ```bash
    docker-compose -f docker-compose-deploy.yml up -d
    ```

## 폴더 구조

```bash
📦Assignment4
 ┣ 📂accounts
 ┃ ┣ 📂migrations
 ┃ ┣ 📂tests
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜tests_account.py
 ┃ ┃ ┣ 📜tests_deposit.py
 ┃ ┃ ┣ 📜tests_tradelog.py
 ┃ ┃ ┗ 📜tests_withdrawal.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜exceptions.py
 ┃ ┣ 📜filters.py
 ┃ ┣ 📜managers.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜permissions.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📂eight_percent
 ┃ ┣ 📂settings
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜base.py
 ┃ ┃ ┣ 📜deploy.py
 ┃ ┃ ┣ 📜dev_local.py
 ┃ ┃ ┗ 📜dev_local_dblog.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜wsgi.py
 ┣ 📂users
 ┃ ┣ 📂migrations
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜permissions.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📜docker-compose-depoly.yml
 ┣ 📜README.md
 ┣ 📜manage.py
 ┣ 📜pull_request_template.md
 ┗ 📜requirements.txt
```

## TIL정리 (Blog)
- 김태우 : 
- 고유영 :
- 박지원 : 
- 최신혁 :
- 박세원 :

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8퍼센트에서 출제한 과제를 기반으로 만들었습니다.
