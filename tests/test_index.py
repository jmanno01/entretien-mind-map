import pytest
from flask import Flask
from app.index import db, Mindmap, Child


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_main_route_status_code(client) -> None:
    route = "/"
    rv = client.get(route)
    assert rv.status_code == 200

@pytest.fixture
def db_client_map():
    app = Flask(__name__)

    app.config["TESTING"] = True
    app.testing = True

    # This creates an in-memory sqlite db
    # See https://martin-thoma.com/sql-connection-strings/
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        map = Mindmap(mindmap_name="study-map")
        db.session.add(map)
        db.session.commit()
    yield client


def test_mindmap(db_client_map) -> None:
    rv = db_client_map.get("/mindmaps")

    result = {
               "Mindmap": [
                 {
                   "id": 1, 
                   "name": "brain-map"
                 }
               ]
             }

    assert rv.json == result


# @pytest.fixture
# def db_client_leaf():
#     app = Flask(__name__)

#     app.config["TESTING"] = True
#     app.testing = True

#     # This creates an in-memory sqlite db
#     # See https://martin-thoma.com/sql-connection-strings/
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

#     client = app.test_client()
#     with app.app_context():
#         db.create_all()
#         child = Child(path="I", text="", mindmap_id=1)
#         db.session.add(child)
#         db.session.commit()
#     yield client


# def test_leaf(db_client_leaf) -> None:
#     rv = db_client_leaf.get("/leaves")
#     result = {
#     "Leaves": [
#             "{'path': 'root/I', 'text': '', 'map_info': mindmap_id=1 | mindmap_name=test-map}"
#         ]
# }
#     assert rv.json == result