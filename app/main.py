from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.schemas import TaskCreate, TaskRead, TaskStatus, TaskUpdate
from app import services

@asynccontextmanager
async def lifespan(_: FastAPI):
    # For this portfolio starter, create missing tables at startup.
    # For production, use a migration tool such as Alembic.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="TaskFlow API",
    description="A task management API demonstrating TDD, modular design, and CI.",
    version="1.0.0",
    lifespan=lifespan,
)

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate, db: DbSession) -> TaskRead:
    return services.create_task(db, payload)


@app.get("/tasks", response_model=list[TaskRead], tags=["tasks"])
def read_tasks(
    db: DbSession,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
) -> list[TaskRead]:
    return services.list_tasks(db, task_status)


@app.get("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def read_task(task_id: int, db: DbSession) -> TaskRead:
    task = services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def edit_task(task_id: int, payload: TaskUpdate, db: DbSession) -> TaskRead:
    task = services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if not payload.model_fields_set:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields supplied")
    return services.update_task(db, task, payload)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def remove_task(task_id: int, db: DbSession) -> Response:
    task = services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    services.delete_task(db, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
