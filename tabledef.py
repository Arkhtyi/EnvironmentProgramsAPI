from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///ProgramDatabase.db')
Base = declarative_base()

# 프로그램 클래스 규정
class Programs(Base):
    __tablename__ = "Programs"
 
    id = Column(Integer, primary_key=True)
    prgm_name = Column(String)      #프로그램명
    theme = Column(String)          #테마별 분류
    region = Column(String)         #서비스 지역
    programSummary = Column(String) #프로그램 소개
    programDetail = Column(String)  #프로그램 상세 소개
    regionCode = Column(String)     #지역 코드

    def __init__(self, prgm_name, theme, region, programSummary, programDetail, regionCode):
        
        self.prgm_name = prgm_name
        self.theme = theme
        self.region = region
        self.programSummary = programSummary
        self.programDetail = programDetail
        self.regionCode = regionCode

