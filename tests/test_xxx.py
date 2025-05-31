from uuid import uuid4, UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyqure import PyqureMemory, pyqure
from todolist_controller import TODOLIST_CONTROLLER, TodolistControllerPort
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation, SubTask
from todolist_hexagon.base.events import EventList
from todolist_hexagon.events import Event


class TodolistControllerDummies(TodolistControllerPort):
    def create_todolist(self) -> UUID:
        raise NotImplementedError()

    def open_task(self, todolist_key: UUID, title: str, description: str) -> UUID:
        raise NotImplementedError()

    def open_sub_task(self, parent_task_key: UUID, title: str, description: str) -> UUID:
        raise NotImplementedError()

    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation | None:
        raise NotImplementedError()

    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        raise NotImplementedError()

    def close_task(self, task_key: UUID) -> None:
        raise NotImplementedError()

    def get_events(self, aggregate_key: UUID) -> EventList[Event]:
        raise NotImplementedError()

    def describe_task(self, task_key: UUID, title: str | None, description: str | None) -> None:
        raise NotImplementedError()


class TodolistControllerForTest(TodolistControllerDummies):
    def __init__(self) -> None:
        self._todolist: dict[UUID, TodolistPresentation] = {}

    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation | None:
        return self._todolist.get(todolist_key, None)

    def feed(self, todolist: TodolistPresentation) -> None:
        self._todolist[todolist.key] = todolist


def test_list_task_when_todolist_exist(app: FastAPI, controller: TodolistControllerForTest, client: TestClient):
    subtask_one = SubTask(key=uuid4(), name="buy the milk", is_opened=False)
    subtask_two = SubTask(key=uuid4(), name="go to the shop", is_opened=True)
    todolist: TodolistPresentation = TodolistPresentation(key=(uuid4()), tasks=[subtask_one, subtask_two])

    controller.feed(todolist)

    response = client.get(f"/todolist/{todolist.key}/task")

    assert response.status_code == 200
    assert response.json() == {
        "todolist":
            {"key": str(todolist.key),
             "tasks": [
                 {"key": str(subtask_one.key), "name": subtask_one.name, "is_opened": subtask_one.is_opened},
                 {"key": str(subtask_two.key), "name": subtask_two.name, "is_opened": subtask_two.is_opened},
             ]}}


def test_list_task_when_todolist_doet_not_exist(app: FastAPI, controller: TodolistControllerForTest,
                                                client: TestClient):
    todolist_key: UUID = uuid4()
    response = client.get(f"/todolist/{todolist_key}/task")

    assert response.status_code == 200
    assert response.json() == {"todolist": {"key": str(todolist_key), "tasks": []}}


def start_app(dependencies: PyqureMemory):
    app = FastAPI()
    (_, inject) = pyqure(dependencies)

    @app.get("/todolist/{todolist_key}/task")
    def list_task(todolist_key) -> dict:
        def get_tasks_or_default(todolist: TodolistPresentation | None) -> list[dict]:
            if todolist is None:
                return []
            return [{"key": str(task.key), "name": task.name, "is_opened": task.is_opened} for task in
                    todolist.tasks]

        controller: TodolistControllerPort = inject(TODOLIST_CONTROLLER)
        todolist = controller.get_todolist(UUID(todolist_key))
        tasks: list = get_tasks_or_default(todolist)
        return {"todolist": {
            "key": todolist_key,
            "tasks": tasks}}

    return app


@pytest.fixture
def app(dependencies: PyqureMemory) -> FastAPI:
    return start_app(dependencies)


@pytest.fixture
def controller() -> TodolistControllerForTest:
    return TodolistControllerForTest()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def dependencies(controller: TodolistControllerForTest) -> PyqureMemory:
    dependencies: PyqureMemory = {}
    (provide, _) = pyqure(dependencies)
    provide(TODOLIST_CONTROLLER, controller)
    return dependencies
