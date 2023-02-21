DROP TABLE IF EXISTS skill_items;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS skills;

CREATE TABLE "users" (
	"name"	TEXT NOT NULL,
	"company"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"phone"	TEXT NOT NULL UNIQUE,
	"user_id"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("user_id")
);

CREATE TABLE "skills" (
	"skill"	TEXT NOT NULL UNIQUE,
	"skills_id"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("skills_id")
);

CREATE TABLE "skill_items" (
	"rating"	INTEGER NOT NULL,
	"user_id"	TEXT NOT NULL,
	"skills_id"	TEXT NOT NULL,
	PRIMARY KEY("user_id", "skills_id")
	FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
	FOREIGN KEY("skills_id") REFERENCES "skills"("skills_id")
);
