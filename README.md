# Jody's Hack The North Backend Challenge Submission

## Linting and Code Formatting
- I use [Black](ms-python.black-formatter) for auto formatting
    - Format the repo with `black .` or `python3 -m black .`
    - Make sure black is installed with `pip install black` or `pip3 install black`
- Also [isort](ms-python.isort) to sort imports and consistent imports
    - Sort imports across the repo with `isort .` or `python3 -m isort .`
    - Make sure black is installed with `pip install isort` or `pip3 install isort`


## Running the Backend
- run the application with 
```docker-compose  up```


## File Structure Layout
```
/jody_htn_backend_challenge
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py      # API Endpoints are here
│   ├── constants/
│   │   ├── query.py
│   |   └── constants.py
│   ├── database/
│   │   ├── db.py
│   │   ├── htn.db
│   │   ├── schema.sql
│   │   ├── HTN_2023_BE_Challenge_Data.json
│   │   ├── skill_items.json
│   │   ├── skills.json
│   |   └── users.json
│   ├── models/
│   |   └── users.py
│   ├── utils/
│   |   └── util.py
├── tests/
│   ├── __init__.py
│   ├── test_api_routes.py
│   └── test_utils.py
├── scripts/
│   └── backfill_btn_db.py
└── run.py
```

## Populate Database
I have script that populates database from the json file provided
```python3 ./scripts/backfill_htn_db.py```

## Run the Tests
run tests (run `pip3 install pytest-mock pytest` if not installed)
```python3 -m pytest```


## Postman Collection
I have provided a postman collection that contains all the possible requests in the file 
```Hack The North 2023 Backend Challenge.postman_collection.json```


## Other
Since there were duplicate skill ratings for some users, the approach taken is only setting the skill with the higher rating, so if we have two cases of python with different skill ratings, we would take the higher rating instead and ignore the lower rating.