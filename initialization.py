from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
import pandas
import os.path




# 데이터베이스 생성
engine = create_engine('sqlite:///ProgramDatabase.db')
Base.metadata.create_all(engine)

session = sessionmaker()
session.configure(bind=engine)
s = session()


# 해당 id 번호를 가진 오브젝트가 이미 데이터베이스에 존재하는지 확인하는 함수
def check_if_exists(id):
    program = s.query(Programs).get(id)

    if program is None:
        return False
    else:
        return True


# 데이터베이스에 csv 파일의 자료 추가
try:

    file_name = 'L10N_Engineering_Pre-Test_국립공원_생태관광_데이터.csv'
    df = pandas.read_csv(file_name, encoding='euc-kr')
    result = df.to_dict('split')
    result1= result['data']

    for i in result1:
        id = i[0]
        if check_if_exists(id) is False:
            record = Programs(i[1], i[2], i[3], i[4], i[5], "undefined")
            s.add(record) #Add all the records
    
    s.commit() #Attempt to commit all the records
except:
    s.rollback() #Rollback the changes on error
finally:
    s.close() #Close the connection
    print ('CSV to Database conversion complete. Any duplicate entries have been ignored')

