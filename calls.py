from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from flask import Flask, request, jsonify
from tabledef import *
from initialization import init_database
import json

DEFAULT_DB = 'sqlite:///ProgramDatabase.db'
TEST_DB = "sqlite:///TestDB.db"

app = Flask(__name__)

#단위 테스트시 메인 데이터베이스가 아닌 테스트용 데이터베이스 생성
s, engine = None, None
if __name__ != '__main__':
        s, engine = init_database(database_name=TEST_DB)
        print ("Initialized testing database")

# API 함수들

# 데이터 추가 
@app.route("/create", methods=['POST'])
def add_new():
        prgm_name = request.json['prgm_name']
        theme = request.json['theme']
        region = request.json['region']
        programSummary = request.json['programSummary']
        programDetail = request.json['programDetail']
        regionCode = request.json['regionCode']

        new_program = Programs(prgm_name, theme, region, programSummary, programDetail,regionCode) 
        

        s.add(new_program)
        s.commit()

        result = {}
        result["prgm_name"] = prgm_name
        result["theme"] = theme
        result["region"] = region
        result["programSummary"] = programSummary
        result["programDetail"] = programDetail
        result["regionCode"] = regionCode

        return jsonify(result)

# 데이터 변경
@app.route("/change", methods=['PUT'])
def update_product():

        id = request.json['id']
        program = s.query(Programs).get(id)

        prgm_name = request.json['prgm_name']
        theme = request.json['theme']
        region = request.json['region']
        programSummary = request.json['programSummary']
        programDetail = request.json['programDetail']
        regionCode = request.json['regionCode']

        program.prgm_name = prgm_name
        program.theme = theme
        program.region = region
        program.programSummary = programSummary
        program.programDetail = programDetail
        program.regionCode = regionCode

        s.commit()

        result = {}
        result["prgm_name"] = prgm_name
        result["theme"] = theme
        result["region"] = region
        result["programSummary"] = programSummary
        result["programDetail"] = programDetail
        result["regionCode"] = regionCode

        return jsonify(result)

# 데이터 조회. 입력한 id 번호의 프로그램을 조회한다
@app.route('/view', methods=['GET'])
def view_program():
        s1 = scoped_session(sessionmaker(bind=engine))
        conn = engine.connect()
        query = conn.execute("SELECT * FROM 'Programs'")

        id = request.json['id']
        program = s1.query(Programs).get(id)

        result = {}
        result["prgm_name"] = program.prgm_name
        result["theme"] = program.theme
        result["region"] = program.region
        result["programSummary"] = program.programSummary
        result["programDetail"] = program.programDetail
        result["regionCode"] = program.regionCode


        return jsonify(result)

# 입력한 지역에서 일어나는 프로그램명과 테마 표시
@app.route('/region', methods=['GET'])
def get_region():

        regionInput = request.json['region']

        conn = engine.connect() # connect to database
        query = conn.execute("SELECT [prgm_name],[theme] FROM 'Programs' WHERE [region] LIKE '%"+regionInput+"%'")
        query1 = conn.execute("SELECT regionCode FROM 'Programs' WHERE [region] LIKE '%"+regionInput+"%'")

        result = {}
        programs_list = []
        region_num = " "
        for regionCode in query1.cursor.fetchall():
                region_num = regionCode[0]
        for program in query.cursor.fetchall(): 
                programs_list.append({"prgm_name": program[0], "theme": program[1].rstrip(",")})

        result["region"] = region_num
        result["programs"] = programs_list

        return jsonify(result)

# 입력한 문자열이 프로그램 소개에 언급되는 서비스 지역과 개수를 표시
@app.route('/keyword1', methods=['GET'])
def get_regionNums():

        keywordInput = request.json['keyword']

        result = {}
        conn = engine.connect() # connect to database
        count = {}
        query = conn.execute("SELECT [region] FROM 'Programs' WHERE [programSummary] LIKE '%"+keywordInput+"%'")
        for region in query.cursor.fetchall():
            try: 
                count[region[0]] = count[region[0]] + 1
            except KeyError: 
                count[region[0]] = 1

        values = [{"region": k, "count": v} for k, v in count.items()]

        result["keyword"] = keywordInput
        result["programs"] = values

        return jsonify(result)

# 입력한 문자열이 프로그램 상세 정보에서 출현하는 빈도수 표시
@app.route('/keyword2', methods=['GET'])
def get_keywordCount():

        keywordInput = request.json['keyword']

        result = {}
        conn = engine.connect() # connect to database
        query = conn.execute("SELECT COUNT(*) FROM 'Programs' WHERE [programDetail] LIKE '%"+keywordInput+"%'")

        for program in query.cursor.fetchall():
                num = program[0]

        result["keyword"] = keywordInput
        result["count"] = num

        return jsonify(result)

# 입력한 id번호에 대응되는 프로그램을 삭제. 기능명세서에 요구되지 않았지만 구현함
@app.route('/delete', methods=['DELETE'])
def delete_program():

        id = request.json['id']

        program = s.query(Programs).get(id)

        s.delete(program)
        s.commit()

        return "deleted"



# flask 서버. 개발용 로컬이기 떄문에 본격적으로 사용시에는 교체할 필요 있음.
if __name__ == '__main__':
        app.run('localhost', 5005)
        s, engine = init_database(database_name=DEFAULT_DB)