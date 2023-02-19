SELECT skills.skills as name, count(*) as frequency from skills, skill_items
group by name

SELECT skills.skills
FROM skills
INNER JOIN skill_items ON skill_items.skills_id=skills.skills_id;


select skills.skills, count(*) from skill_items, skills
where skill_items.skills_id = skills.skills_id
group by skills.skills


select skills.skill as skill, count(*) as frequency from skill_items, skills
where skill_items.skills_id = skills.skills_id
group by skill
having frequency > 30 and frequency < 40
order by frequency desc


select rating, skill from users, skill_items, skills
where users.user_id = skill_items.user_id AND skills.skills_id=skill_items.skills_id and users.user_id = "c19d085d-d65d-4a53-8202-91a197125dec"