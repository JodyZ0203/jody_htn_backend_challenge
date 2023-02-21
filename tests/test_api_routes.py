from run import app


def test_get_list_of_users():
    with app.test_client() as c:
        response = c.get("/users")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) == 1000


def test_get_skill_items(mocker):
    mock_skill_items = [
        {
            "rating": 4,
            "user_id": "e4dff847-4039-4d04-98c9-eef8a33c5d83",
            "skills_id": "f56be422-d1c4-4b6d-a919-e5f3b0d714dc",
        },
        {
            "rating": 3,
            "user_id": "e4dff847-4039-4d04-98c9-eef8a33c5d83",
            "skills_id": "722b700d-6682-4236-a517-347ea460e941",
        },
    ]
    mocker.patch("app.api.routes.query_db", return_value=mock_skill_items)
    with app.test_client() as c:
        response = c.get("/skill_items")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) == 2


def test_get_skill_list(mocker):
    mock_skills_list = [
        {"skill": "Swift", "skills_id": "86695e88-0465-4162-9c2d-c40db4765fb0"},
        {"skill": "OpenCV", "skills_id": "bd5513d5-26e2-4aa8-976d-7d6e0e099656"},
        {"skill": "Foundation", "skills_id": "ba16f8fe-81b9-4f2e-afcc-22d20897745f"},
    ]
    mocker.patch("app.api.routes.query_db", return_value=mock_skills_list)
    with app.test_client() as c:
        response = c.get("/skills_list")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) == 3


def test_get_skill_frequency(mocker):
    mock_skills_list = [
        {"skill": "Swift", "frequency": 4},
        {"skill": "OpenCV", "frequency": 5},
    ]
    mocker.patch("app.api.routes.query_db", return_value=mock_skills_list)
    with app.test_client() as c:
        response = c.get("/skills")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) == 2


def test_get_lucky_users():
    with app.test_client() as c:
        response = c.get("/users/random/1")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) == 1


def test_get_multiple_lucky_users():
    with app.test_client() as c:
        response = c.get("/users/random/10")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) == 10


def test_get_user_skills_by_id(mocker):
    mock_user_info = {
        "name": "Lori Monroe",
        "company": "Santos, Huber and Green",
        "email": "greenedward@example.net",
        "phone": "(230)555-1203",
        "skills": [
            {"rating": 3, "skill": "Smalltalk"},
            {"rating": 3, "skill": "OCaml"},
            {"rating": 1, "skill": "Haskell"},
        ],
    }
    user_id = "566f2ece-d0b0-4c3b-b5a0-c1ad2fb6d346"
    mocker.patch("app.api.routes.query_db", return_value=mock_user_info)
    with app.test_client() as c:
        response = c.get(f"/skills/{user_id}")
        assert response.status_code == 200
        json_response = response.get_json()
        assert json_response == mock_user_info


def test_get_user_data_by_id(mocker):
    user_id = "566f2ece-d0b0-4c3b-b5a0-c1ad2fb6d346"
    mock_user_skills = [
        {"rating": 4, "skill": "ASP.NET"},
        {"rating": 3, "skill": "Unity"},
        {"rating": 1, "skill": "Ant Design"},
        {"rating": 3, "skill": "Jinja"},
        {"rating": 2, "skill": "Flask"},
        {"rating": 4, "skill": "ChatGPT"},
    ]
    mock_user_info = {
        "name": "Lori Monroe",
        "company": "Santos, Huber and Green",
        "email": "greenedward@example.net",
        "phone": "(230)555-1203",
        "skills": [
            {"rating": 3, "skill": "Smalltalk"},
            {"rating": 3, "skill": "OCaml"},
            {"rating": 1, "skill": "Haskell"},
        ],
        "user_id": user_id,
    }
    mocker.patch("app.api.routes.query_db", return_value=mock_user_info)
    mocker.patch("app.api.routes.get_user_skills", return_value=mock_user_skills)
    with app.test_client() as c:
        response = c.get(f"/users/{user_id}")
        assert response.status_code == 200
        json_response = response.get_json()
        assert json_response == mock_user_info


def test_get_user_data_by_id_json_error():
    user_id = "test"
    with app.test_client() as c:
        response = c.get(f"/users/{user_id}")
        assert response.status_code == 400
        json_response = response.get_json()
        assert json_response == f"This user_id {user_id} is not valid uuid"


def test_get_user_skills_by_id_json_error():
    user_id = "test"
    with app.test_client() as c:
        response = c.get(f"/skills/{user_id}")
        assert response.status_code == 400
        json_response = response.get_json()
        assert json_response == f"This user_id {user_id} is not valid uuid"
