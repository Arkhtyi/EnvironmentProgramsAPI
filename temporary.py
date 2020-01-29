from flask import request, jsonify
from calls import app


with app.test_client() as c:
    json_data = {"prgm_name" : "프로그램1",	"theme" : "테마1", "region" : "지역1", "programSummary": "프로그램소개1", "programDetail": "프로그램상세1",	"regionCode" : "지역코드어딘가"}
    rv = c.post("/create", json=json_data)
    result = rv.get_json()
    assert verify_token(result, json_data)