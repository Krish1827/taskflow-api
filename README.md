# TaskFlow API

A portfolio project demonstrating Python REST API development, test-driven development (TDD), modular design, automated testing, and CI with GitHub Actions.

## Stack

- Python 3.12
- FastAPI and Pydantic
- SQLAlchemy 2
- PostgreSQL for Docker Compose; SQLite for a simple local run and isolated tests
- pytest and FastAPI TestClient
- Docker and GitHub Actions

## Features

- Create, list, retrieve, update, and delete tasks
- Filter tasks by status (`pending`, `in_progress`, `completed`)
- Request validation and useful HTTP errors
- Health endpoint at `/health`
- Automated tests for CRUD operations, invalid input, filtering, and missing records
- CI workflow runs tests on pushes and pull requests

## Run locally (SQLite)

Requires Python 3.12 or newer.

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, or run `.venv\Scripts\python.exe` directly.

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Run with Docker Compose and PostgreSQL

Requires Docker Desktop to be running.

```powershell
docker compose up --build
```

Then open http://localhost:8000/docs. Stop services with `Ctrl+C`; remove the containers with `docker compose down`. To also remove the local database volume, run `docker compose down -v` (this permanently deletes the stored local database data).

The example database credentials are for local development only. Do not use them for a public deployment.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API status |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks |
| GET | `/tasks?status=completed` | Filter tasks by status |
| GET | `/tasks/{task_id}` | Retrieve one task |
| PATCH | `/tasks/{task_id}` | Update supplied fields |
| DELETE | `/tasks/{task_id}` | Delete a task |

Example request:

```json
{
  "title": "Practice test-driven development",
  "description": "Write a failing test before implementation"
}
```

## TDD workflow to practice

For each new feature:

1. Write a test describing the expected behavior.
2. Run the test and observe it fail for the expected reason (red).
3. Write the smallest implementation that makes it pass (green).
4. Refactor for readability and design while keeping tests green.
5. Commit the change with a descriptive message.

The included tests provide a baseline. To demonstrate authentic TDD, add a new test first when extending the project, and use small commits to record your process.

## Design notes

- `main.py` defines HTTP routes and translates missing-resource conditions into HTTP responses.
- `schemas.py` validates incoming data and shapes API responses.
- `services.py` contains task operations and database interactions.
- `models.py` defines the persistence model.
- `database.py` centralizes database configuration and session creation.

This separation keeps responsibilities clearer and makes the code easier to test. Apply SOLID principles where they genuinely improve the design; avoid adding abstractions that don't solve a real problem.

## Next improvements

- Add Alembic migrations instead of creating tables at startup.
- Add pagination and more filtering.
- Add API-level integration tests against PostgreSQL.
- Add code formatting/linting (Ruff) and coverage reporting.
- Add a deployment stage after deciding on a hosting platform.
- Add authentication only if it serves a clear project requirement.

## Honest project scope

This is a learning and portfolio starter, not a production service. It does not include authentication, authorization, rate limiting, production secrets management, or database migrations.
