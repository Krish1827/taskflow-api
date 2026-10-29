def test_create_and_get_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Prepare portfolio", "description": "Add tests"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Prepare portfolio"
    assert created["description"] == "Add tests"
    assert created["status"] == "pending"
    assert created["id"] > 0

    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


def test_title_cannot_be_blank(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_title_is_required(client):
    response = client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 422


def test_list_tasks_and_filter_by_status(client):
    first = client.post("/tasks", json={"title": "Write tests"}).json()
    second = client.post("/tasks", json={"title": "Ship feature"}).json()
    client.patch(f"/tasks/{second['id']}", json={"status": "completed"})

    all_response = client.get("/tasks")
    completed_response = client.get("/tasks?status=completed")

    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    assert [task["id"] for task in completed_response.json()] == [second["id"]]


def test_update_task(client):
    task = client.post("/tasks", json={"title": "Old title"}).json()

    response = client.patch(f"/tasks/{task['id']}", json={"title": "New title", "status": "in_progress"})

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["status"] == "in_progress"


def test_update_rejects_invalid_status(client):
    task = client.post("/tasks", json={"title": "Valid task"}).json()

    response = client.patch(f"/tasks/{task['id']}", json={"status": "blocked"})

    assert response.status_code == 422


def test_missing_task_returns_404(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(client):
    task = client.post("/tasks", json={"title": "Delete me"}).json()

    delete_response = client.delete(f"/tasks/{task['id']}")
    get_response = client.get(f"/tasks/{task['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_update_without_fields_returns_400(client):
    task = client.post("/tasks", json={"title": "Keep me"}).json()

    response = client.patch(f"/tasks/{task['id']}", json={})

    assert response.status_code == 400
