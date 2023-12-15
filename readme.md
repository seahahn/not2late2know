# ❇️ Not 2 Late 2 Know

## 1️⃣ Project Introduction

- A web application created to raise awareness about the escalating climate change among a wider audience
- Includes information on key elements of climate change, such as global average temperature, greenhouse gases, Arctic sea ice area, and sea level rise
- Visit: ~~[not2late2know.herokuapp.com](https://not2late2know.herokuapp.com)~~
  - Because of the server cost, it is temporarily closed

<br/>

## 2️⃣ Development Period & Team

- Dec 3, 2021 - Dec 13, 2021
- Personal project

<br/>

## 3️⃣ 사용 기술

| Category     | Technology                                    |
| ------------ | --------------------------------------------- |
| Frontend     | HTML/CSS/JS, Chart.js 3.6.2                   |
| Backend      | Flask 2.0.2, APScheduler 3.8.1, Python 3.8.10 |
| Database     | PostgreSQL(ElephantSQL)                       |
| DevOps       | Heroku                                        |
| Data Science | Pandas 1.3.4, Scikit-Learn 1.0.1              |

<br/>

## 4️⃣ Service Architecture

![not2late2know_service_structure](https://private-user-images.githubusercontent.com/73585246/290913351-2c1b6d36-da3c-4aba-874c-95ef1836a616.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDI2NjcwMDgsIm5iZiI6MTcwMjY2NjcwOCwicGF0aCI6Ii83MzU4NTI0Ni8yOTA5MTMzNTEtMmMxYjZkMzYtZGEzYy00YWJhLTg3NGMtOTVlZjE4MzZhNjE2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMTUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjE1VDE4NTgyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTMxZTQ5OGViNjNjY2FiYTliMzczM2I5YTllMGM1ZjQ0NTZlODcwNWY5OTM4NjVlZmM1Mjk5NWFjOGI2NDkyMmImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.y188kwre1uZKgk0f73HWyfUdgDN3QdzuLWJPvF09Qb4)

1. Data related to climate change elements, obtained from the API provided by global-warming.org and downloaded from the U.S. Environmental Protection Agency (EPA), is stored in a cloud database (ElephantSQL-PostgreSQL based)
   - Except for sea level rise, all other data is periodically and automatically updated using APScheduler (Advanced Python Scheduler)
2. API services based on the retrieved data:
   - API service that sends data in JSON format
   - API service for predicting values using a machine learning model, which sends predicted results when values are entered according to the input form
3. Provides visualization of each data item in charts and a dashboard page where all charts can be viewed in one place
4. Deployment using Heroku ~~(https://not2late2know.herokuapp.com/)~~

<br/>

## 5️⃣ API Usage

- Base URL : ~~[not2late2know.herokuapp.com/](https://not2late2know.herokuapp.com/)~~
- Enter the path corresponding to the desired API after the base URL.
  - e.g., Get global average temperature data: not2late2know.herokuapp.com/api/global-temp/
- {desired_value}: Enter the value corresponding to the data you want to retrieve.
  - In case of incorrect input, an error message will be displayed.
  - {int:whatever} -> Should enter an integer.
  - ex. e.g., Global average temperature data for October 2010: not2late2know.herokuapp.com/api/global-temp/2010/10

### 1) Fetch JSON Data (GET)

1. Global Average Temperature

```
- All data : /api/global-temp/
- Specific year data : /api/global-temp/{int:year}
- Specific year/month data : /api/global-temp/{int:year}/{int:month}
```

2. Atmospheric Carbon Dioxide Amount

```
- All data : /api/co2/
- Specific year data : /api/co2/{int:year}
- Specific year/month data : /api/co2/{int:year}/{int:month}
- Specific year/month/day data : /api/co2/{int:year}/{int:month}/{int:day}
```

3. Atmospheric Methane Amount

```
- All data : /api/methane/
- Specific year data : /api/methane/{int:year}
- Specific year/month data : /api/methane/{int:year}/{int:month}
```

4. Atmospheric Nitrous Oxide Amount

```
- All data : /api/nitrous/
- Specific year data : /api/nitrous/{int:year}
- Specific year/month data : /api/nitrous/{int:year}/{int:month}
```

5. Arctic Sea Ice Area

```
- All data : /api/sea-ice/
- Specific year data : /api/sea-ice/{int:year}
```

6. Sea Level Rise

```
- All data : /api/sea-level/
- Specific year data : /api/sea-level/{int:year}
```

### 2) Predict Values Using Machine Learning Model (GET)

1. Global Average Temperature

```
/ml/global-temp/?year={int:year}&month={int:month}
```

2. Atmospheric Carbon Dioxide Amount

```
/ml/co2/?year={int:year}&month={int:month}&day={int:day}
```

3. Atmospheric Methane Amount

```
/ml/methane/?year={int:year}&month={int:month}
```

4. Atmospheric Nitrous Oxide Amount

```
/ml/nitrous/?year={int:year}&month={int:month}
```

## 6️⃣ Project Demo Video (Click to Watch)

[![Project Not2Late2Know Presentation](https://user-images.githubusercontent.com/73585246/160866813-34ec2c18-b5cf-4978-831f-f9cfa18443d2.PNG)](https://youtu.be/6v5VtH4JQr4)
