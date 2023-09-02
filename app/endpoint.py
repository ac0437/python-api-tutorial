from fastapi.testclient import TestClient
import main
client = TestClient(main.app)


# def test_home_path():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello WorldS"}
