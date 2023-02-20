import sqlite3
import uuid

def get_skills(dataset: dict)-> list:
    skills_id_dict = {}
    for data in dataset:
        for skills in data["skills"]:
            skill = skills["skill"]
            if skill not in skills_id_dict:
                skills_id_dict[skill] = str(uuid.uuid4())

    return skills_id_dict


def populate_skills(skills_dict: dict)-> None:
    connection = sqlite3.connect('../app/database/htn.db')

    cur = connection.cursor()
    for key, val in skills_dict.items():
        cur.execute("INSERT INTO skills(skills_id, skill) VALUES  (?,?)", (val, key))

    connection.commit()
    connection.close()


def process_users_and_ratings(data: dict, skills_dict: dict)-> dict:
    skills_list = []
    for user in data:
        id = str(uuid.uuid4()) 
        user["user_id"] = id
        skills = user["skills"]
        user.pop("skills")
        skills = sorted(skills, key=lambda d: d['rating'], reverse=True) 
        for skill in skills:
            skills_id = skills_dict[skill["skill"]]
            skill["skills_id"] = skills_id
            skill["user_id"] = id
            skill.pop("skill")
            skills_list.append(skill)
            connection = sqlite3.connect('../app/database/htn.db')

            cur = connection.cursor()
            cur.execute("INSERT OR IGNORE INTO skill_items (skills_id, user_id, rating) VALUES  (?,?,?)", (skills_id ,id, skill["rating"]))

            connection.commit()
            connection.close()
        connection = sqlite3.connect('../app/database/htn.db')

        cur = connection.cursor()
        cur.execute("INSERT INTO users (user_id, name, email, company, phone) VALUES  (?,?,?,?,?)", (id, user["name"], user["email"], user["company"], user["phone"]))

        connection.commit()
        connection.close()
    return data, skills_list


if __name__ == "__main__":
    import json
    data = json.load(open('../app/database/HTN_2023_BE_Challenge_Data.json', 'r'))
    skills_dict = {'Swift': '86695e88-0465-4162-9c2d-c40db4765fb0', 'OpenCV': 'bd5513d5-26e2-4aa8-976d-7d6e0e099656', 'Foundation': 'ba16f8fe-81b9-4f2e-afcc-22d20897745f', 'Elixir': '0a901935-db41-4a88-9fdb-72fecb87291c', 'Fortran': '4f1fc444-375f-4dfe-a2bd-888d4d4deffa', 'Plotly': '722b700d-6682-4236-a517-347ea460e941', 'Haskell': '9773b535-f88e-442a-b00a-ee530b288f0e', 'PHP': 'c5fad8bc-7258-4cb4-81fe-7d360db9b139', 'Scheme': 'ac02646c-7294-40f1-9e71-302146e4c077', 'Julia': '30008abc-9570-439d-8352-98723c5ed642', 'Spectre.css': '27686108-60c9-42d3-9a71-30a63f9297c2', 'Ruby': '96e52b23-8e1f-4ca5-913f-9640e6fde47f', 'Sed': '1724a733-3a00-43d4-ae7a-ab7a2b9e7b15', 'Smalltalk': '583d880f-ebed-4ac0-b0d6-db707a0af57a', 'Materialize': 'bd2efeab-7fde-41a7-ba56-461bb433a3d5', 'Svelte': '2f9344db-a739-40ae-a647-de483c0e636c', 'Unreal Engine': '0b99d0b0-679f-4641-b657-20e74cd1aa85', 'Unity': '1594dea5-9f30-457c-a93f-f526fae082ea', 'ASP.NET': '15071b13-d410-45c8-aaea-e2b8e7f46542', 'AutoHotkey': '512b2073-3e62-423d-be13-3185a3aa655a', 'Angular': 'bc682aed-2043-4709-adac-0bcf64a53a5b', 'Ant Design': '36ac9ebc-ee47-4ad2-a5dd-55c545574acc', 'OCaml': '8e808481-5b3b-49e4-940d-48767d6d5778', 'Tornado': '9f490eff-d99a-4af8-9657-64458546f137', 'Theano': 'c13b5717-cd48-4b1f-bd35-722efbaa81c6', 'Sanic': '1cb63ac1-a559-4c4b-8780-4a628c566bc0', 'SQL': 'a88fd7ec-fb7e-4065-8f7e-eff60a03fffd', 'Nest.js': 'abe06adb-e71a-4325-9d9e-394f864118f9', 'Element UI': '019d57c5-b0c4-4bfe-baad-3f3c4240907a', 'Ruby on Rails': '3e6f2f63-f971-48cc-82a9-db7b4026f920', 'C++': '2aef9d9f-2402-441e-8378-abcae0f35fa1', 'Spring Boot': 'aab64449-9532-4431-9aca-81478ac3d907', 'Go': '01d04f09-2fd9-457b-890c-76fa091a8dd1', 'Chakra UI': 'adb67f74-6fce-4497-8561-006d95a3f415', 'Vue.js': 'e454545e-ed1b-48a4-a813-e66b7a749318', 'Buefy': 'afaeee69-b24c-4473-9b02-e151af61e440', 'AutoIt': 'de9291f8-e242-4e7e-abc3-b44ef74ff8e0', 'Django': 'bb416b23-d072-43c0-a54c-2181a947a2af', 'Erlang': 'e510cf7a-46a3-4829-81c1-dee6a7f3cb8f', 'Numpy': '45818203-2985-4ae4-b18d-172b6089babf', 'C#': 'df728adf-6bd0-454f-875e-c34d6c1569be', 'Express.js': '50bed349-51dd-49b4-825b-b005d89a48db', 'Gensim': '3e3c6e22-334b-4ec7-92c6-66425c1b75b1', 'Clojure': 'fde4b62f-8a4e-4bc6-a445-3f32c1e6c808', 'Tcl': 'f56be422-d1c4-4b6d-a919-e5f3b0d714dc', 'Lua': '2fd38a90-3f3f-4fcb-8a04-6337767162bc', 'Kotlin': '5bae503a-391d-4f8b-9341-f1cb534fec86', 'Awk': 'a78afaec-fc82-4662-8f15-e18f09fb086b', 'Milligram': '1a65a002-c794-4b09-a7c7-7bff27642b09', 'Pygame': 'a7fb1cf8-8bf9-4596-8b6e-b2db664e1d1f', 'Java': '61811fce-ecbd-4162-a637-7c4056d4acc5', 'SciPy': '281b82d8-3d65-4dd0-a953-16d86588ceac', 'Bash': 'e0c7c480-265e-409a-b1a5-557178e8d63f', 'Godot': 'dd6e6c01-9688-495b-b034-6a5222e2b2d2', 'Spacy': '7e088f78-ffeb-471d-bf6a-212161758b28', 'Backbone.js': 'b12b3ac2-19d0-4944-a97a-a19d7882e2c9', 'R': '94367dfc-704b-4fdb-b8bf-66875f8f9d16', 'C': 'b37e8eb3-5459-4db5-a8d3-d838ea4e77e2', 'React': 'b789beae-c963-462c-9377-1fd207030a69', 'Laravel': '3597e3c8-c67b-43f6-be93-17ba04e4ad82', 'Bulma': '14ba96b3-5015-4a47-8556-976a4972eaf6', 'Objective-C': '1a762c41-8720-4e16-b3d3-731f15688e8d', 'Rust': '5d1c8625-79de-4432-ba2e-dcb8bf20aa67', 'F#': 'ba361eb0-4cf4-4509-9a61-c60c1e82c62c', 'Starlette': '343265fa-aa30-4ebd-ab65-69dc3f5b34e8', 'Scala': '8ad704c9-e949-43d1-9e42-7b0b3480b0d2', 'PyTorch': '26062f6e-5fff-4f78-a11e-421207f6bca7', 'Common Lisp': 'f2f846f0-5ad3-46b9-a04b-23ac4d949365', 'Semantic UI': 'e3d7ca46-4034-4164-9c1b-b683f848c30d', 'Flask-RESTful': '8d6d98dd-d2e1-4f1d-acb3-ef597585c768', 'Ember.js': '59382c44-2b72-4d81-9b8a-0b51d236a78b', 'Scikit-learn': '16c7ca66-d88e-4928-99d8-0ac4b8c7f688', 'Pascal': 'fadec17f-a05e-43c5-8efd-e34e14ce2a47', 'Bokeh': 'fbb4ac49-3662-4a34-b71e-a16f5635a26b', 'Tachyons': '7798bb6d-90ef-4d99-9540-f5ee71b4c1a4', 'FastAPI': '77f68ef3-e3b7-4309-8424-7d0f474e43de', 'Dart': 'ad8c7f29-87a7-4a2e-8032-c45c43f127b2', 'Flask': 'a45e2ca8-36d9-4386-a681-97a5d60f6af7', 'mini.css': 'd2d4d973-26df-4355-901b-1423f5f6f0df', 'Keras-RL': '9a50b86b-8d7b-4e3f-81d4-118101898217', 'Perl': 'aa51f157-1266-429a-aca8-5fd03cbb7fae', 'TypeScript': '71002c3a-7c50-45a3-8785-270ba8d7c14a', 'Polymer': 'af9ed12c-3138-4546-889b-14fa08488f34', 'Logo': '07f7da23-f5ee-4be7-8299-6643f3e3a2d1', 'TensorFlow': '17dbe570-caeb-49a5-b07f-f677864e5299', 'COBOL': '679aaae5-7604-428c-9243-349607f1eac3', 'NLTK': 'c305cdba-6725-42ad-bee3-97f424060f06', 'JavaScript': '416397e0-5a79-4f2e-866c-51ae7fb1fe1a', 'Keras': '8f1c3c8e-c770-4216-8449-afd468d4e417', 'Bootstrap': '2e63aa99-b5b4-4508-bd37-856fd19b6101', 'Matplotlib': '583ebd2b-bf93-4a45-a83b-af1a96157d3d', 'Assembly': '30dc7e60-ffc6-4bd6-bb5c-37e28bcba1b6', 'Visual Basic': 'da81ce55-87fd-4750-8a65-9fea50e7bcd4', 'Pandas': 'ab634e2e-75c9-4a81-8dd4-b4b87f26ce8a', 'Django REST framework': '4baafa05-2ebb-410e-ba9c-748746c78876', 'Ada': '1c3381ce-a341-4bbd-aed3-a4104d0e3b5d', 'Node.js': 'e36da6ee-e1e8-4efb-be97-ddfd36fdfa0e', 'Prolog': '25f3888c-82fa-4304-9e20-adec067dd7da', 'Next.js': '6f319335-7ab0-4574-abc1-791e6169562d', 'Python': '5f24d436-838b-4db6-87c0-c5db5a47a2f7', 'Tailwind': '9f28d855-70a0-4185-9cbb-f2fc148b36e6', 'Elm': '93269a94-7917-487b-9955-a473dcbdee50', 'Aurelia': 'db946412-8860-4867-b633-10e942fa5feb', 'Meteor': '0c5b43a7-a271-43bf-a7cb-0db02bd9ed84', 'Seaborn': 'b8524637-6bc5-415a-a45a-e2968c592838', 'Lisp': 'a055ac4d-2f1d-4d7a-bea4-3ef2aa84e85b'}
    #dictionary = get_skills(data)
    populate_skills(skills_dict)
    user_data, skills = process_users_and_ratings(data, skills_dict)
    print(skills)
    print(user_data)
    #populate_skills(dictionary)

    '''
    data = json.load(open('../app/database/skill_items.json', 'r'))
    for skill in data:
            connection = sqlite3.connect('../app/database/htn.db')

            cur = connection.cursor()
            print(skill["user_id"])
            cur.execute("INSERT OR IGNORE INTO test_items (skill_id, user_id, rating) VALUES  (?,?,?)", (skill["skills_id"] ,skill["user_id"], skill["rating"]))
            print(skill["user_id"])
            connection.commit()
            connection.close() 
    '''
