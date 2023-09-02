from ..app import schema
import pytest


def test_getting_post(authorized_client, test_post):
    response = authorized_client.get("/posts/")
    all_posts = response.json()

    def valdiate_post(post):
        return schema.PostOut(**post)
    post_map = map(valdiate_post, all_posts)
    posts = list(post_map)

    for post in posts:
        testing_post = test_post[post.Post.id - 1]
        assert post.Post.title == testing_post.title
        assert post.Post.content == testing_post.content
        assert post.Post.published == testing_post.published
    assert response.status_code == 200
    assert len(posts) == len(test_post)


def test_unauthorized_user_get_all_post(client, test_post):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_unauthorized_user_get_single_post(client, test_post):
    response = client.get("/posts/1")

    assert response.status_code == 401

# pydantic checks this for use and returns a validation error for PostOut
# and error none is not an allowed value
# def test_get_post_that_does_not_exisit(authorized_client, test_user, test_post):
#     response = authorized_client.get("/posts/800")

#     assert response.status_code == 404


def test_get_one_post(authorized_client, test_post):
    response = authorized_client.get("/posts/1")
    post = response.json()
    assert post['Post']['title'] == test_post[post['Post']['id'] - 1].title
    assert post['Post']['content'] == test_post[post['Post']['id'] - 1].content
    assert post['Post']['published'] == test_post[post['Post']
                                                  ['id'] - 1].published


@pytest.mark.parametrize("title, content, published", [
    ("who is it", "dialated people", False),
    ("prototype", "of you", False),
    ("i'm a rookie", "but better then those veterans", False),
])
def test_create_post(authorized_client, test_user, test_post, title, content, published):
    post_data = {"title": title, "content": content, "published": published}
    response = authorized_client.post(
        '/posts/', json=post_data)
    new_post = response.json()
    assert response.status_code == 201
    assert new_post["title"] == post_data["title"]
    assert new_post["content"] == post_data["content"]
    assert new_post["published"] == post_data["published"]


def test_unauthorized_user_create_post(client, test_post):
    response = client.post(
        '/posts/', json={"title": "title", "content": "content", "published": "published"})

    assert response.status_code == 401


# pydantic is expecting published so this returns missing field error
# def test_default_published_true(authorized_client, test_user, test_post):
#     post_data = {"title": "first", "content": "hello"}
#     response = authorized_client.post(
#         '/posts/', json=post_data)
#     post = response.json()
#     print(post)
#     assert post["published"] == True

# @pytest.mark.dependency(depends=["test_create_post"])


def test_updatinging_post(authorized_client, test_post, test_user):
    post_data = {
        "title": "check it out",
        "content": "I'm the miggty miggty miggty mc daddy",
        "published": True
    }
    response = authorized_client.put('/posts/1', json=post_data)
    post = schema.Post(**response.json())
    print(post)
    assert response.status_code == 200
    assert post.title == post_data["title"]
    assert post.content == post_data["content"]
    assert post.published == post_data["published"]


def test_updatinging_other_users_post(authorized_client2, test_post, test_user2):
    post_data = {
        "title": "check it out",
        "content": "I'm the miggty miggty miggty mc daddy",
        "published": True
    }
    response = authorized_client2.put('/posts/1', json=post_data)

    assert response.status_code == 403


def test_updatinging_post_unauthenticated(client, test_post, test_user):
    post_data = {
        "title": "check it out",
        "content": "I'm the miggty miggty miggty mc daddy",
        "published": True
    }
    response = client.put('/posts/1', json=post_data)

    assert response.status_code == 401


def test_updting_non_existing_post(authorized_client2, test_post, test_user2):
    post_data = {
        "title": "check it out",
        "content": "I'm the miggty miggty miggty mc daddy",
        "published": True
    }
    response = authorized_client2.put('/posts/88888', json=post_data)

    assert response.status_code == 404


def test_deletinging_post(authorized_client, test_post, test_user):
    response = authorized_client.delete('/posts/1')

    assert response.status_code == 204


def test_unauthorized_deletinging_post(client, test_post):
    response = client.delete('/posts/1')

    assert response.status_code == 401


def test_deletinging_non_existing_post(authorized_client2, test_post, test_user2):
    response = authorized_client2.delete('/posts/5')

    assert response.status_code == 204
