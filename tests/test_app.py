from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Basic smoke checks
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "tester@example.com"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate sign-up should fail
    res2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res2.status_code == 400

    # Unregister
    res3 = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert res3.status_code == 200
    assert email not in activities[activity]["participants"]
