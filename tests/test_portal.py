import pytest
from app import app, load_submissions

VALID = {"name": "Ali", "reg_no": "FA23-BSE-001", "title": "Lab 1",
         "url": "https://github.com/ali/lab1"}


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["DATA_FILE"] = str(tmp_path / "submissions.json")
    return app.test_client()


def test_valid_submission_is_saved_and_listed(client):
    r = client.post("/", data=VALID)
    assert r.status_code == 200
    assert b"Submission saved" in r.data
    page = client.get("/").data
    assert b"FA23-BSE-001" in page and b"https://github.com/ali/lab1" in page


def test_missing_registration_number_is_rejected(client):
    r = client.post("/", data={**VALID, "reg_no": ""})
    assert r.status_code == 400
    assert b"Registration number is required" in r.data
    assert load_submissions() == []


def test_invalid_url_is_rejected_and_not_saved(client):
    r = client.post("/", data={**VALID, "url": "not-a-url"})
    assert r.status_code == 400
    assert b"Submission URL is not valid" in r.data
    assert load_submissions() == []
