from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 以降のテストで使うためにIDを保存する変数（TSの let targetId: number; に相当）
target_id = None


def test_1_POST_新規TODOを追加できるか():
    # 関数外の target_id を更新するために global 宣言をします
    global target_id

    response = client.post(
        "/api/todos",
        json={"title": "テストタスク"}
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "テストタスク"
    assert data["done"] is False
    
    # 以降のテストで使うためにIDを保存
    target_id = data["id"]


def test_2_GET_追加したTODOが取得できるか():
    response = client.get("/api/todos")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    assert any(todo["id"] == target_id and todo["title"] == "テストタスク" and todo["done"] is False for todo in data)


def test_3_PUT_追加したTODOの完了状態を切り替えられるか():
    response = client.put(f"/api/todos/{target_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == target_id
    assert data["title"] == "テストタスク"
    assert data["done"] is True 

def test_4_DELETE_追加したTODOを削除できるか():
    response = client.delete(f"/api/todos/{target_id}")
    
    assert response.status_code == 200
    
    response = client.get("/api/todos")
    data = response.json()
    assert not any(todo["id"] == target_id for todo in data)

def test_5_POST_空文字のタイトルはエラーになるか():
    response = client.post(
        "/api/todos",
        json={"title": "   "}  # 空白だけのタイトル
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "タイトルは必須です"