import unittest
import os
import json
from initialization import init_database
from calls import app
from flask import Flask
from flask_testing import TestCase
import os

#단위 테스트 파일. 실행시 테스트용 데이터베이스인 Test.DB가 생성됨

class ProgramsUnitTest(TestCase):


        def create_app(self):
                return app

        def setUp(self):
                self.app = self.create_app()
                pass

        def test_add_new(self):
                
                json_data = {"prgm_name" : "프로그램1",	"theme" : "테마1", "region" : "지역1", "programSummary": "프로그램소개1", "programDetail": "프로그램상세1",	"regionCode" : "지역코드어딘가"}
                result = self.app.test_client().post('/create',  data = json.dumps(json_data), content_type='application/json' )
                data = json.loads(result.get_data(as_text=True))
                self.assertEqual(result.status_code, 200)
                self.assertEqual(data, json_data)
                
        
        #데이터 변경 테스트
        def test_update_product(self):
                json_data = {"id" : 1,
                        "prgm_name" : "수정프로그램1",	  
                        "theme" : "수정테마1",
                        "region" : "수정지역1",
                        "programSummary": "수정프로그램소개1",
                        "programDetail": "수정프로그램상세1",
                        "regionCode" : "수정지역코드어딘가"
                        }
                
                result_data = {
                        "prgm_name" : "수정프로그램1",	  
                        "theme" : "수정테마1",
                        "region" : "수정지역1",
                        "programSummary": "수정프로그램소개1",
                        "programDetail": "수정프로그램상세1",
                        "regionCode" : "수정지역코드어딘가"
                        }
                response = app.test_client().put('/change',  data = json.dumps(json_data), content_type='application/json' )

                data = json.loads(response.get_data(as_text=True))


                self.assertEqual(response.status_code, 200)
                self.assertEqual(data, result_data)


        #데이터 조회 테스트
        def test_view_program(self):
                json_data = {
                        "id": 13
                        }

                result_data = {
                        "prgm_name": "오대산국립공원 힐링캠프",
                        "programDetail": " 천년의 숲으로 불리는 오대산 전나무숲과 선재길에서 다양한 숲치유 프로그램 체험",
                        "programSummary": "선재길, 한국자생식물원, 전나무숲, 월정사, 방아다리약수",
                        "region": "강원도 평창군 진부면",
                        "regionCode": "undefined",
                        "theme": "숲 치유,"
                }
                response = app.test_client().get('/view',  data = json.dumps(json_data), content_type='application/json' )


                data = json.loads(response.get_data(as_text=True))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(data, result_data)

        #기능명세 함수 1번 테스트
        def test_region(self):
                json_data = {
                        "region":"평창군"
                        }

                result_data = {
                        "programs": [
                        {
                        "prgm_name": "오감만족! 오대산 에코 어드벤처 투어",
                        "theme": "아동·청소년 체험학습"
                        },
                        {
                        "prgm_name": "오대산국립공원 힐링캠프",
                        "theme": "숲 치유"
                        },
                        {
                        "prgm_name": "소금강 지역문화 체험",
                        "theme": "자연생태"
                        },
                        {
                        "prgm_name": "(1박2일)자연으로 떠나는 행복여행",
                        "theme": "문화생태체험,자연생태체험"
                        }
                ],
                "region": "undefined"
                }

                response = app.test_client().get('/region',  data = json.dumps(json_data), content_type='application/json' )
                data = json.loads(response.get_data(as_text=True))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(data, result_data)

        #기능명세 함수 2번 테스트
        def test_get_regionNums(self):
                json_data = {
                        "keyword":"견학"
                        }

                result_data = {
                        "keyword": "견학",
                        "programs": [
                        {
                                "count": 1,
                                "region": "경상남도 통영"
                        },
                        {
                                "count": 2,
                                "region": "전라남도 장성군 북하면 백양로 1116"
                        }
                        ]
                }

                response = app.test_client().get('/keyword1',  data = json.dumps(json_data), content_type='application/json' )
                data = json.loads(response.get_data(as_text=True))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(data, result_data)

        #기능명세 함수 3번 테스트
        def test_get_keywordCount(self):
                json_data = {
                        "keyword":"탐방"
                        }

                result_data = {
                        "count": 14,
                        "keyword": "탐방"
                }

                response = app.test_client().get('/keyword2',  data = json.dumps(json_data), content_type='application/json' )
                data = json.loads(response.get_data(as_text=True))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(data, result_data)
        

if __name__ == "__main__":
    unittest.main()