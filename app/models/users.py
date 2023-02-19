from typing import TypedDict

class Skill(TypedDict):
    skill: str
    rating: int


class User(TypedDict):
    name: str
    company: str
    email: str
    phone: str
    skills: Skill