from uuid import UUID

from todolist_controller import TodolistControllerPort
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation
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
