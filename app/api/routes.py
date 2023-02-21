import json
import uuid
from typing import List

from flask import Blueprint, request

import app.utils.util as util
from app.database.db import execute_query, query_db
from app.models.users import Skill, User

bp = Blueprint("", __name__)


@bp.route("/")
def hello_world():
    return "<p>Hello, World! This is Jody's submission to the HTN Backend Challenge."


@bp.route("/users/random/<int:number_of_winners>", methods=["GET"])
def get_lucky_users(number_of_winners):
    number_of_winners = 1 if not number_of_winners else int(number_of_winners)
    query = """Select * FROM users ORDER by random() LIMIT ?"""
    result = query_db(query, (number_of_winners,))
    return util.send_json(result)


@bp.route("/skill_items")
def get_skill():
    query = """SELECT * FROM skill_items"""
    result = query_db(query)
    return json.dumps(result)


@bp.route("/skills_list")
def get_skillitems():
    query = """SELECT * FROM skills"""
    result = query_db(query)
    return json.dumps(result)


@bp.route("/skills", methods=["GET"])
def get_skill_freq():
    int_max = 2147483647
    args = request.args
    try:
        max_freq = int(args.get("max_frequency", int_max))
        min_freq = int(args.get("min_frequency", 0))
    except ValueError as e:
        return util.json_error(500, str(e))

    query = """SELECT skills.skill AS skill, count(*) AS frequency FROM skill_items, skills
    WHERE skill_items.skills_id = skills.skills_id
    GROUP BY skill
    HAVING frequency < ? AND frequency > ?
    ORDER BY frequency DESC
    """
    skills = query_db(query, (max_freq, min_freq))
    return util.send_json(skills)


@bp.route("/skills/<user_id>", methods=["GET"])
def get_user_skills(user_id: uuid, flag: bool = False) -> List[Skill]:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    query = """SELECT rating, skill FROM users, skill_items, skills
WHERE users.user_id = skill_items.user_id AND skills.skills_id=skill_items.skills_id AND users.user_id = ?"""

    skills = query_db(query, (user_id,))
    if flag:
        return skills
    return util.send_json(skills)


@bp.route("/users/<user_id>", methods=["GET"])
def get_user_information(user_id: uuid, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")

    query = """SELECT * FROM users
WHERE user_id = ?"""
    user = query_db(query, (user_id,), True)
    skills = get_user_skills(user_id, True)
    user["skills"] = skills
    user.pop("user_id")
    if flag:
        return user
    return util.send_json(user)


@bp.route("/users")
def get_users():
    query = """SELECT * FROM users"""
    users = query_db(query)
    for user in users:
        user_id = user.pop("user_id")
        skills = get_user_skills(user_id, True)
        user["skills"] = skills
    return util.send_json(users)


@bp.route("/test/<user_id>", methods=["GET"])
def get_user_information_test(user_id: uuid, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    query = """SELECT * FROM users
WHERE user_id = ?"""
    user = query_db(query, user_id, True)
    skills = get_user_skills(user_id, True)
    user["skills"] = skills
    if flag:
        return user
    return util.send_json(user)


@bp.route("/skills/<user_id>", methods=["PUT"])
def update_skills(user_id: uuid, skills: Skill = None, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    request_body = json.loads(request.data)
    skills = request_body.get("skills", skills)

    for skill in skills:
        skill_id = str(uuid.uuid4())
        skill_name = skill["skill"]
        skill_rating = skill["rating"]
        query1 = "INSERT OR IGNORE INTO skills(skill, skills_id) VALUES(?, ?)"
        execute_query(query1, (skill_name, skill_id))
        skill_id = query_db(
            "SELECT skills_id FROM skills WHERE skill = ?", (skill_name,), True
        )["skills_id"]
        query2 = (
            "INSERT INTO skill_items(user_id, skills_id, rating) "
            + f"VALUES('{user_id}', '{skill_id}', {skill_rating}) "
            + "ON CONFLICT (user_id, skills_id) DO "
            + f"UPDATE SET rating={skill_rating};"
        )
        execute_query(query2)
    return "Success"


@bp.route("/users/<user_id>", methods=["PUT"])
def update_user_information(user_id: uuid, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    request_body = json.loads(request.data)
    skills = request_body.get("skills", None)
    request_body.pop("skills")
    query_component = []
    for key, val in request_body.items():
        query_component.append(f"{key} = '{val}'")
    query_components = ",".join(query_component)
    query = "UPDATE users " + f"SET {query_components} " f"WHERE user_id='{user_id}';"
    execute_query(query)
    update_skills(user_id, skills)
    return get_user_information(user_id, True)
