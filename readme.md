# ❇️ Not 2 Late 2 Know

## 1️⃣ 작품 소개

- 갈수록 심해지는 기후 변화에 대하여 보다 많은 사람들에게 경각심을 주기 위한 목적으로 만들어진 웹 어플리케이션
- 기후 변화에 관한 주요 요소들 중 세계 평균 기온, 온실 가스, 북극 해빙 면적 그리고 해수면 높이에 대한 내용 수록

<br/>

## 2️⃣ 제작 기간 & 참여 인원
- 2021.12.03 - 2021.12.13
- 개인 프로젝트

<br/>

## 3️⃣ 사용 기술

| 분류 | 기술 목록 |
| --- | --- |
| Frontend | HTML/CSS/JS, Chart.js 3.6.2 |
| Backend | Flask 2.0.2, APScheduler 3.8.1, Python 3.8.10 |
| Database | PostgreSQL(ElephantSQL) |
| DevOps | Heroku |
| Data Science | Pandas 1.3.4, Scikit-Learn 1.0.1 |

<br/>

## 4️⃣ 서비스 구조

![not2late2know_service_structure](https://user-images.githubusercontent.com/73585246/145774815-c99ba9d5-182c-4ec7-a127-9d297e8859fc.png)

1. global-warming.org에서 제공하는 API 및 미국 환경 보호국(EPA)에서 다운로드 받은 기후 변화 관련 요소 데이터를 클라우드 데이터베이스(ElephantSQL-PostgreSQL 기반)에 저장
   - 해수면 높이를 제외한 나머지 데이터는 APScheduler(Advanced Python Scheduler)를 통해 주기적으로 자동 갱신
2. 가져온 데이터를 바탕으로 API 서비스 제공
   1. JSON 형태로 데이터를 보내주는 API 서비스
   2. 입력 양식에 맟추어 값 입력 시 예측 결과를 보내주는 머신 러닝 모델을 통한 값 예측 API 서비스
3. 각각의 데이터 항목을 차트로 표현 & 모든 차트를 한 곳에서 확인 가능한 대시보드 페이지 제공
   1. 북극 해빙 면적 추가 시각화 앱 제공 (https://livingatlas.arcgis.com/sea-ice/)
   2. 해수면 높이 추가 시각화 앱 제공 (https://csb-6kq9k.netlify.app/)-Origin from :(https://openlayers.org/en/latest/examples/webgl-sea-level.html)
4. Heroku를 통한 배포 (https://not2late2know.herokuapp.com/)

<br/>

## 5️⃣ API 사용법

- Base URL : [not2late2know.herokuapp.com/](https://not2late2know.herokuapp.com/)
- Base URL 뒤에 원하는 API에 해당하는 경로를 입력하시면 됩니다.
  - ex. 세계 평균 기온 전체 데이터 가져오기 : not2late2know.herokuapp.com/api/global-temp/
- {원하는_값} : 원하는_값 안에 가져올 데이터에 해당하는 값을 입력하세요.
  - 올바르지 않은 입력값인 경우 오류 메시지 출력
  - {int:whatever} -> 정수(integer)를 입력해야 합니다.
  - ex. 세계 평균 기온 2010년 10월 데이터 : not2late2know.herokuapp.com/api/global-temp/2010/10

### 1) JSON 데이터 가져오기(GET)

1. 세계 평균 기온
```
- 전체 데이터 : /api/global-temp/
- 특정 년도 데이터 : /api/global-temp/{int:year}
- 특정 년/월 데이터 : /api/global-temp/{int:year}/{int:month}
```

2. 대기 중 이산화탄소 양
```
- 전체 데이터 : /api/co2/
- 특정 년도 데이터 : /api/co2/{int:year}
- 특정 년/월 데이터 : /api/co2/{int:year}/{int:month}
/api/co2/{int:year}/{int:month}/{int:day}
```

3. 대기 중 메탄 양
```
- 전체 데이터 : /api/methane/
- 특정 년도 데이터 : /api/methane/{int:year}
- 특정 년/월 데이터 : /api/methane/{int:year}/{int:month}
```

4. 대기 중 아산화질소 양
```
- 전체 데이터 : /api/nitrous/
- 특정 년도 데이터 : /api/nitrous/{int:year}
- 특정 년/월 데이터 : /api/nitrous/{int:year}/{int:month}
```

5. 북극 해빙 면적
```
- 전체 데이터 : /api/sea-ice/
- 특정 년도 데이터 : /api/sea-ice/{int:year}
```

6. 해수면 높이
```
- 전체 데이터 : /api/sea-level/
- 특정 년도 데이터 : /api/sea-level/{int:year}
```

### 2) 머신 러닝 모델을 통한 값 예측(GET)

1. 세계 평균 기온
```
/ml/global-temp/?year={int:year}&month={int:month}
```

1. 대기 중 이산화탄소 양
```
/ml/co2/?year={int:year}&month={int:month}&day={int:day}
```

3. 대기 중 메탄 양
```
/ml/methane/?year={int:year}&month={int:month}
```

4. 대기 중 아산화질소 양
```
/ml/nitrous/?year={int:year}&month={int:month}
```

## 6️⃣ 프로젝트 시연 영상 (클릭 시 이동)
[![Project Not2Late2Know Presentation](https://user-images.githubusercontent.com/73585246/160866813-34ec2c18-b5cf-4978-831f-f9cfa18443d2.PNG)](https://youtu.be/6v5VtH4JQr4)
