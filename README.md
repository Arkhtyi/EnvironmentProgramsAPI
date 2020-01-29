# 생태 정보 서비스 API

제공된 국립공원 생태 데이터를 기반으로 데이터베이스를 생성하고 데이터베이스에 데이터를 추가/수정/조회 및 몇 가지 추가기능이 가능한 API 입니다. Python 3.8.1을 기반으로 개발되었습니다.


# 빌드 및 실행 방법

1. git clone https://github.com/Arkhtyi/EnvironmentProgramsAPI.git
2. pip install pandas flask sqlalchemy
3. python initialization.py
4. python calls.py
5. http://127.0.0.1:5005/ 으로 접속해서 API 활용


# 기능 명세 및 각 기능의 문제 해결 전략

* 데이터 파일에서 각 레코드를 데이터베이스에 저장하는 API 를 개발하세요.
  * 제약사항에 명시된 대로 각 레코드를 ORM을 사용하여 저장하기 위해서 SQLAlchemy를 기반으로 오브젝트 클래스(Programs)를 규정했습니다.
  * Programs 클래스는 데이터 파일의 각 프로그램 정보에 대응하여 prgm_name(프로그램명), theme(테마별 분류), region(서비스 지역), programSummary(프로그램 소개), programDetail(프로그램 상세 소개), regionCode(지역 코드) 변수를 가지도록 규정했습니다. 
  * SQLAlchemy를 이용하여 SQLite3 데이터베이스 파일을 로컬에 생성하고 제공된 csv 데이터 파일을 읽어들여 개별적으로 위에서 규정된 Programs 오브젝트로 구현하고 데이터베이스 파일에 추가하는 방식으로 구현했습니다. (단, 지역 코드 변수에 대해서는 규정과 구현방법에 대한 정보가 부족하여 현재는 전부 "undefined"로만 채워넣었지만, 지역 코드 변수 자체는 구현 해놓음으로써 향후 지역 코드의 정의가 확정되면 수정이 용이하도록 유연성을 가지고 구현했습니다.)
  * 데이터 파일의 데이터베이스화는 initialization.py 파일에서 이루어지며 혹시나 파일의 데이터가 중복으로 수록되는 것을 방지하도록 조치했습니다.
  
* 생태 관광정보 데이터를 조회/추가/수정할 수 있는 API 를 개발하세요. 단, 조회는 서비스 지역 코드를 기준으로 검색합니다
  * HTTP Method들을 이용해서 데이터베이스에서 데이터의 조회/추가/수정을 구현했습니다.
  * 조회 기능
    * 조회 기능은 json 데이터를 입력하여 /view로 요청하도록 구현했습니다 ('GET' 사용) (__기능명세서에서는 지역 코드를 기준으로 검색할 것을 명시했지만, 현재 지역 코드가 정확히 규정되지 않은 탓에 임시로 지역코드가 아닌 id 번호로 조회하도록 설정해 놓았습니다. 향후 수정 가능__)
     * 입력 예시 
         ```
        {
          "id": 13
        }
         ```
     * 출력 예시  
         ```
        {
            "prgm_name": "오대산국립공원 힐링캠프",
            "programDetail": " 천년의 숲으로 불리는 오대산 전나무숲과 선재길에서 다양한 숲치유 프로그램 체험",
            "programSummary": "선재길, 한국자생식물원, 전나무숲, 월정사, 방아다리약수",
            "region": "강원도 평창군 진부면",
            "regionCode": "undefined",
            "theme": "숲 치유,"
        }
         ```
  
  * 추가 기능
    * 추가 기능은 추가할 데이터를 json 데이터의 형태로 입력하고 /create로 추가를 요청하도록 구현했습니다('POST' 사용)   
     * 입력 예시
        ```
       {
        "prgm_name" : "프로그램1",
        "theme" : "테마1",
        "region" : "지역1",
        "programSummary": "프로그램소개1",
        "programDetail": "프로그램상세1",
        "regionCode" : "지역코드어딘가"
       }
        ```
     * 결과물 예시  
       ![alt text](https://github.com/Arkhtyi/EnvironmentProgramsAPI/blob/master/Readme%20Images/postResult.JPG)
       추가 요청한 데이터가 데이터베이스에 추가 된 모습
       
  * 수정 기능
    * 수정 기능은 수정할 항목의 id와 데이터를 json 데이터의 형태로 입력하고 /change로 수정을 요청하도록 구현했습니다('PUT' 사용)   
     * 입력 예시
     ```
       {
        "id" : 1,
        "prgm_name" : "수정프로그램1",	  
        "theme" : "수정테마1",
        "region" : "수정지역1",
        "programSummary": "수정프로그램소개1",
        "programDetail": "수정프로그램상세1",
        "regionCode" : "수정지역코드어딘가"
       }
     ```
     * 결과물 예시  
        ![alt text](https://github.com/Arkhtyi/EnvironmentProgramsAPI/blob/master/Readme%20Images/putResult.JPG)
        수정 요청한 데이터가 데이터베이스에 적용 된 모습

