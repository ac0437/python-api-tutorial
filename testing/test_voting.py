import pytest


def test_voting_on_post(authorized_client, test_post):
    response = authorized_client.post("/votes/", json={"post_id": 1, "dir": 1})

    assert response.json()['message'] == 'successful vote'


def test_unauthorized_voting_on_post(client, test_post):
    response = client.post("/votes/", json={"post_id": 1, "dir": 1})

    assert response.status_code == 401


def test_voting_post_not_found(authorized_client, test_post):
    response = authorized_client.post(
        "/votes/", json={"post_id": 888, "dir": 1})

    assert response.status_code == 404
    assert response.json().get('detail') == "Post not found."


def test_voting_vote_not_found(authorized_client, test_post):
    response = authorized_client.post(
        "/votes/", json={"post_id": 1, "dir": 0})

    assert response.status_code == 404
    assert response.json().get('detail') == "Vote not found."


def test_voting_on_post(authorized_client, test_post):
    response = authorized_client.post("/votes/", json={"post_id": 1, "dir": 1})
    response2 = authorized_client.post(
        "/votes/", json={"post_id": 1, "dir": 1})

    assert response2.status_code == 409
    assert response2.json().get('detail') == "Post already voted on."


def test_voting_deleted_vote(authorized_client, test_post):
    response = authorized_client.post("/votes/", json={"post_id": 1, "dir": 1})
    response2 = authorized_client.post(
        "/votes/", json={"post_id": 1, "dir": 0})

    assert response2.status_code == 201


def test_voting_liked(authorized_client, test_post):
    response = authorized_client.post("/votes/1")

    assert response.json() == "liked"


def test_voting_liked_not_found(authorized_client, test_post):
    response = authorized_client.post("/votes/888")

    assert response.status_code == 404
    assert response.json().get("detail") == "Post not found."


def test_voting_liked_unauthorized(client, test_post):
    response = client.post("/votes/1")

    assert response.status_code == 401
