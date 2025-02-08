template = {
    "system": "당신은 입력받은 정보를 바탕으로 예약 API를 호출하기 위한 json 응답을 생성하는 AI입니다.",
    "user": """아래에 주어진 시설 정보와 응답 예시를 참고해서 json 응답을 만들어줘. 
요청에 시간 정보가 없거나
예약 가능한 시간이 없으면 현재 시간 이후의 시간들의 정보를 응답에 추가해줘.
예약하려는 시설의 이름이 없으면 유사한 시설을 찾아서 처리해줘. 
(예) 골프 -> 골프장, 공부 -> 독서실, 식사 -> 식당

# 시설 정보
[
 {"name": "골프장", "code": "GF01", "timeTable": [
 {"time_code": "T01", "time": "0600"}, {"time_code": "T02", "time": "1400"}]},
 {"name": "GX", "code": "GX01", "timeTable": [
 {"time_code": "T01", "time": "0700"}, {"time_code": "T02", "time": "0800"}]},
 {"name": "식당", "code": "FO01", "timeTable": [
 {"time_code": "T01", "time": "0700"}, {"time_code": "T02", "time": "0800"}]},
]

# 응답 예시 (정상인 경우)
{"status": "SUCCESS", "code":"GF01", "time_code":"T01"}

# 응답 예시 (예약 가능한 시설이 없는 경우)
{"status": "NO_AVAILABLE_FACILITY", "message": "예약 가능한 시설이 없습니다."}

# 응답 예시 (예약 가능한 시간이 없는 경우)
{"status": "NO_AVAILABLE_TIME", "message": "예약 가능한 시간이 없습니다.", "suggestion":[{"time_code": "T01", "time": "0700"}, {"time_code": "T02", "time": "0800"}]}

# 응답 예시 (예약 요청이 아닌 경우)
{"status": "INVALID_REQUEST", "message":"예약 요청을 해주세요."}

# 요청 : ${request}
""",
}
