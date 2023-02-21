QUERY_LUCKY_WINNER = """Select * FROM users ORDER by random() LIMIT ?"""
QUERY_SKILL_ITEMS = """SELECT * FROM skill_items"""
QUERY_SKILLS = """SELECT * FROM skills"""
QUERY_USERS = """SELECT * FROM users"""
QUERY_SKILLS_FREQUENCY = """SELECT skills.skill AS skill, count(*) AS frequency FROM skill_items, skills
                            WHERE skill_items.skills_id = skills.skills_id
                            GROUP BY skill
                            HAVING frequency < ? AND frequency > ?
                            ORDER BY frequency DESC
                        """
QUERY_SKILLS_BY_USER_ID = """SELECT rating, skill FROM users, skill_items, skills
                             WHERE users.user_id = skill_items.user_id AND skills.skills_id=skill_items.skills_id AND users.user_id = ?"""
QUERY_USER_BY_USER_ID = """SELECT * FROM users WHERE user_id = ?"""
QUERY_INSERT_NEW_SKILL = (
    """INSERT OR IGNORE INTO skills(skill, skills_id) VALUES(?, ?)"""
)
QUERY_SKILL_ID_BY_SKILL = """SELECT skills_id FROM skills WHERE skill = ?"""
