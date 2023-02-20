import json
import sqlite3
from typing import List
import uuid
from flask import Blueprint, request
from app.models.users import Skill, User
import app.utils.util as util
from app.database.db import execute_query, get_db, query_db
from app.database.skills import skills_dict
from scripts.backfill_htn_db import process_users_and_ratings

bp = Blueprint('', __name__)


@bp.route("/")
def hello_world():
    return "<p>Hello, World! This is Jody's submission to the HTN Backend Challenge You can click the following links to checkout some get methods<ul> <li> <a href='/skills'>GET skill frequency</a></li><a href='/skills?min_frequency=5&max_frequency=50'>GET skill requency with param filtering</a></li></ul></p>"


@bp.route('/users/random/<int:number_of_winners>', methods=["GET"])
def get_lucky_users(number_of_winners):
    number_of_winners = 1 if not number_of_winners else int(number_of_winners)
    connection = sqlite3.connect('app/database/htn.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    sqlite = """Select * from users
ORDER by random() limit ?"""
    rows = cur.execute(sqlite, (number_of_winners,)).fetchall()
    connection.close()
    return util.send_json([dict(ix) for ix in rows]) #CREATE JSON

@bp.route('/skills')
def get_skill():
    
    connection = sqlite3.connect('app/database/htn.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    sqlite = """SELECT * from skill_items"""

    rows = cur.execute(sqlite).fetchall()
    connection.close()
    return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON

@bp.route('/skillitems')
def get_skillitems():
    
    connection = sqlite3.connect('app/database/htn.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    sqlite = """SELECT * from skills"""

    rows = cur.execute(sqlite).fetchall()
    connection.close()
    return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON


@bp.route('/skills', methods=["GET"])
def get_skill_freq():
    int_max = 2147483647 
    args = request.args
    try:
        max_freq = int(args.get("max_frequency", int_max))
        min_freq = int(args.get("min_frequency", 0))
    except ValueError as e:
        return util.json_error(500, str(e))
    
    connection = sqlite3.connect('app/database/htn.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    sql = """select skills.skill as skill, count(*) as frequency from skill_items, skills
    where skill_items.skills_id = skills.skills_id
    group by skill
    having frequency < ? and frequency > ?
    order by frequency desc
    """

    rows = cur.execute(sql, (max_freq, min_freq)).fetchall()
    connection.close()
    skills = [dict(ix) for ix in rows] 

    return util.send_json(skills) #CREATE JSON

@bp.route('/skills/<user_id>', methods=["GET"])
def get_user_skills(user_id: uuid, flag: bool = False) -> List[Skill]:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    connection = sqlite3.connect('app/database/htn.db')

    cur = connection.cursor()
    cur.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    query = """select rating, skill from users, skill_items, skills
where users.user_id = skill_items.user_id AND skills.skills_id=skill_items.skills_id and users.user_id = ?"""
    row = cur.execute(query, (user_id,)).fetchall()
    skills = [dict(ix) for ix in row]
    connection.close()
    if flag:
        return skills
    return util.send_json(skills) #CREATE JSON

@bp.route('/users/<user_id>', methods=["GET"])
def get_user_information(user_id: uuid, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    connection = sqlite3.connect('app/database/htn.db')

    cur = connection.cursor()
    cur.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    query = """select * from users
where user_id = ?"""
    row = cur.execute(query, (user_id,)).fetchall()
    user = [dict(ix) for ix in row][0]
    skills = get_user_skills(user_id, True)
    user["skills"] = skills 
    connection.close()
    user.pop("user_id")
    if flag:
        return user
    return util.send_json(user) #CREATE JSON

@bp.route('/users')
def get_users():
    #connection = get_db()
    #cur = connection
    #cur = connection.cursor()
    #cur.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    sqlite = """SELECT * from users"""

    #rows = cur.execute(sqlite).fetchall()
    users = query_db(sqlite)
     #users = [dict(ix) for ix in rows]
    for user in users:
        user_id = user.pop("user_id")
        skills = get_user_skills(user_id, True)
        user["skills"] = skills

    
    #connection.close()

    return util.send_json(users) #CREATE JSON

@bp.route('/test/<user_id>', methods=["GET"])
def get_user_information_test(user_id: uuid, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    query = """select * from users
where user_id = ?"""
    user = query_db(query, user_id, True)
    skills = get_user_skills(user_id, True)
    user["skills"] = skills 
    if flag:
        return user
    return util.send_json(user) #CREATE JSON

@bp.route('/skills/<user_id>', methods=["PUT"])
def update_skills(user_id: uuid, skills: Skill=None, flag: bool = False) -> User:
    if not util.is_uuid(user_id):
        return util.json_error(400, f"This user_id {user_id} is not valid uuid")
    request_body = json.loads(request.data)
    skills = request_body.get("skills", skills)

    for skill in skills:
        skill_id = str(uuid.uuid4())
        skill_name = skill["skill"]
        skill_rating = skill["rating"]
        # add new skill to skill table if not exists in it already
        query1 = "INSERT OR IGNORE INTO skills(skill, skills_id) VALUES(?, ?)"
        execute_query(query1, (skill_name, skill_id))
        skill_id = query_db("select skills_id from skills where skill = ?", (skill_name,), True)["skills_id"]
        #test = query_db("select skills_id from skills where skill = ?", (skill_name,))
        #query1 = "INSERT OR IGNORE INTO skills(skill, skills_id) VALUES(?, ?)"
        #connection = get_db()
        #cur = connection.cursor()
        #cur.execute(query1, (skill_name, skill_id))
        #execute_query(query1, (skill_id, skill_name))
        #return test
        query2 = "INSERT INTO skill_items(user_id, skills_id, rating) " +  f"VALUES('{user_id}', '{skill_id}', {skill_rating}) " + "ON CONFLICT (user_id, skills_id) DO " + f"UPDATE SET rating={skill_rating};"
        #return query2
        execute_query(query2)
    
        # update skills for user

    return "Success"

    # update skill rating if exists
    # create new skill dict if doesnt exist
    # add new skill for this person


@bp.route('/users/<user_id>', methods=["PUT"])
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
    sql = ("UPDATE users " + 
       f"SET {query_components} "
       f"WHERE user_id='{user_id}';")
    #return sql
    # execute this sql
    execute_query(sql)
    update_skills(user_id, skills)
    return get_user_information(user_id, True) 
    # update skill rating if exists
    # create new skill dict if doesnt exist
    # add new skill for this person

    '''
    query = """select * from users
where user_id = ?"""
    user = query_db(query, user_id, True)
    skills = get_user_skills(user_id, True)
    user["skills"] = skills 
    if flag:
        return user
    return util.send_json(user) 
    '''