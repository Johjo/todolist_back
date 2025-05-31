from uuid import uuid4, UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyqure import PyqureMemory, pyqure
from todolist_controller import TODOLIST_CONTROLLER
from todolist_controller.presentation.todolist import TodolistPresentation, SubTask

from tests.todolist_controller_dummies import TodolistControllerDummies
from todolist_back.app import start_app


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


@pytest.fixture
def app(dependencies: PyqureMemory) -> FastAPI:
    return start_app(dependencies)


@pytest.fixture
def controller(dependencies: PyqureMemory) -> TodolistControllerForTest:
    (provide, _) = pyqure(dependencies)
    controller = TodolistControllerForTest()
    provide(TODOLIST_CONTROLLER, controller)
    return controller


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def dependencies() -> PyqureMemory:
    dependencies: PyqureMemory = {}
    return dependencies
