import json
import uuid
from typing import List

from flask import Blueprint, request

import app.utils.util as util
from app.constants.constants import INT_MAX
from app.constants.query import (
    QUERY_INSERT_NEW_SKILL,
    QUERY_LUCKY_WINNER,
    QUERY_SKILL_ID_BY_SKILL,
    QUERY_SKILL_ITEMS,
    QUERY_SKILLS,
    QUERY_SKILLS_BY_USER_ID,
    QUERY_SKILLS_FREQUENCY,
    QUERY_USER_BY_USER_ID,
    QUERY_USERS,
)
from app.database.db import execute_query, query_db
from app.models.users import Skill, User

bp = Blueprint("", __name__)


@bp.route("/")
def hello_world():
    return "<p>Hello, World! This is Jody's submission to the HTN Backend Challenge."


@bp.route("/users/random/<int:number_of_winners>", methods=["GET"])
def get_lucky_users(number_of_winners):
    number_of_winners = 1 if not number_of_winners else int(number_of_winners)
    result = query_db(QUERY_LUCKY_WINNER, (number_of_winners,))
    return util.send_json(result)


@bp.route("/skill_items")
def get_skill():
    result = query_db(QUERY_SKILL_ITEMS)
    return json.dumps(result)


@bp.route("/skills_list")
def get_skillitems():
    result = query_db(QUERY_SKILLS)
    return json.dumps(result)


@bp.route("/skills", methods=["GET"])
def get_skill_freq():
    args = request.args
    try:
        max_freq = int(args.get("max_frequency", INT_MAX))
        min_freq = int(args.get("min_frequency", 0))
    except ValueError as e:
        return util.json_error(500, str(e))

    skills = query_db(QUERY_SKILLS_FREQUENCY, (max_freq, min_freq))
    return util.send_json(skills)


@bp.route("/skills/<user_id>", methods=["GET"])
def get_user_skills(user_id: uuid, flag: bool = False) -> List[Skill]:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")

    skills = query_db(QUERY_SKILLS_BY_USER_ID, (user_id,))
    if flag:
        return skills
    return util.send_json(skills)


@bp.route("/users/<user_id>", methods=["GET"])
def get_user_information(user_id: uuid, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")

    user = query_db(QUERY_USER_BY_USER_ID, (user_id,), True)
    skills = get_user_skills(user_id, True)
    user["skills"] = skills
    user.pop("user_id")
    if flag:
        return user
    return util.send_json(user)


@bp.route("/users")
def get_users():
    users = query_db(QUERY_USERS)
    for user in users:
        user_id = user.pop("user_id")
        skills = get_user_skills(user_id, True)
        user["skills"] = skills
    return util.send_json(users)


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
        execute_query(QUERY_INSERT_NEW_SKILL, (skill_name, skill_id))
        skill_id = query_db(QUERY_SKILL_ID_BY_SKILL, (skill_name,), True)["skills_id"]
        upsert_query = (
            "INSERT INTO skill_items(user_id, skills_id, rating) "
            + f"VALUES('{user_id}', '{skill_id}', {skill_rating}) "
            + "ON CONFLICT (user_id, skills_id) DO "
            + f"UPDATE SET rating={skill_rating};"
        )
        execute_query(upsert_query)
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
