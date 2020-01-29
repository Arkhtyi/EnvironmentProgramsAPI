from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
import pandas
import os.path

DEFAULT_DB = 'sqlite:///ProgramDatabase.db'
DEFAULT_CSV = 'L10N_Engineering_Pre-Test_국립공원_생태관광_데이터.csv'

# 데이터베이스 생성 및 csv 파일의 자료 추가
def init_database(csv=DEFAULT_CSV, database_name=DEFAULT_DB):

    engine = create_engine(database_name)
    Base.metadata.create_all(engine)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    # 해당 id 번호를 가진 오브젝트가 이미 데이터베이스에 존재하는지 확인하는 helper function
    def check_if_exists(id):
        program = s.query(Programs).get(id)

        if program is None:
            return False
        else:
            return True

    try:

        df = pandas.read_csv( csv , encoding='euc-kr')
        result = df.to_dict('split')
        result1= result['data']

        for i in result1:
            id = i[0]
            if check_if_exists(id) is False:
                record = Programs(i[1], i[2], i[3], i[4], i[5], "undefined")
                s.add(record) 
        
        s.commit() 
    except:
        s.rollback() 
    finally:
        s.close() 

    return (s, engine)


