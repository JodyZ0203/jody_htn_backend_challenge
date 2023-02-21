import sqlite3
import uuid
import json

DATABASE = "../app/database/htn.db"


def get_skills(dataset: dict) -> list:
    skills_id_dict = {}
    for data in dataset:
        for skills in data["skills"]:
            skill = skills["skill"]
            if skill not in skills_id_dict:
                skills_id_dict[skill] = str(uuid.uuid4())

    return skills_id_dict


def populate_skills(skills_dict: dict) -> None:
    connection = sqlite3.connect(DATABASE)

    cur = connection.cursor()
    for key, val in skills_dict.items():
        cur.execute("INSERT INTO skills(skills_id, skill) VALUES  (?,?)", (val, key))

    connection.commit()
    connection.close()


def process_users_and_ratings(data: dict, skills_dict: dict) -> dict:
    skills_list = []
    for user in data:
        id = str(uuid.uuid4())
        user["user_id"] = id
        skills = user["skills"]
        user.pop("skills")
        skills = sorted(skills, key=lambda d: d["rating"], reverse=True)
        for skill in skills:
            skills_id = skills_dict[skill["skill"]]
            skill["skills_id"] = skills_id
            skill["user_id"] = id
            skill.pop("skill")
            skills_list.append(skill)
            connection = sqlite3.connect(DATABASE)
            cur = connection.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO skill_items (skills_id, user_id, rating) VALUES  (?,?,?)",
                (skills_id, id, skill["rating"]),
            )
            connection.commit()
            connection.close()
        connection = sqlite3.connect(DATABASE)
        cur = connection.cursor()
        cur.execute(
            "INSERT INTO users (user_id, name, email, company, phone) VALUES  (?,?,?,?,?)",
            (id, user["name"], user["email"], user["company"], user["phone"]),
        )
        connection.commit()
        connection.close()
    return data, skills_list


if __name__ == "__main__":
    data = json.load(open("../app/database/HTN_2023_BE_Challenge_Data.json", "r"))
    skills_dict = get_skills(data)
    populate_skills(skills_dict)
    user_data, skills = process_users_and_ratings(data, skills_dict)
