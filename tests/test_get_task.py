from uuid import uuid4, UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyqure import PyqureMemory, pyqure
from todolist_controller import TODOLIST_CONTROLLER
from todolist_controller.presentation.task import TaskPresentation, SubTask

from tests.todolist_controller_dummies import TodolistControllerDummies
from todolist_back.app import start_app


class TodolistControllerForTest(TodolistControllerDummies):
    def __init__(self) -> None:
        self.tasks : dict[UUID, TaskPresentation] = {}

    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        return self.tasks.get(task_key, None)

    def feed(self, task: TaskPresentation) -> None:
        self.tasks[task.key] = task


def test_list_task_when_task_exist(app: FastAPI, controller: TodolistControllerForTest, client: TestClient):
    subtask_one = SubTask(key=uuid4(), name="buy the milk", is_opened=False)
    subtask_two = SubTask(key=uuid4(), name="go to the shop", is_opened=True)
    main_task: TaskPresentation = TaskPresentation(key=uuid4(), name="buy the milk", subtasks=[subtask_one, subtask_two], is_opened=True)

    controller.feed(main_task)

    response = client.get(f"/task/{main_task.key}")

    assert response.status_code == 200
    assert response.json() == {
        "task":
            {"key": str(main_task.key),
             "is_opened": main_task.is_opened,
             "subtasks": [
                 {"key": str(subtask_one.key), "name": subtask_one.name, "is_opened": subtask_one.is_opened},
                 {"key": str(subtask_two.key), "name": subtask_two.name, "is_opened": subtask_two.is_opened},
             ]}}


def test_list_task_when_task_does_not_exist(app: FastAPI, controller: TodolistControllerForTest,
                                                client: TestClient):
    task_key: UUID = uuid4()
    response = client.get(f"/task/{task_key}")

    assert response.status_code == 200
    assert response.json() == {"task": {"key": str(task_key), "subtasks": [], "is_opened": False}}


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
