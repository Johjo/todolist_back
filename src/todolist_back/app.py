from uuid import UUID

from fastapi import FastAPI
from pyqure import PyqureMemory, pyqure
from todolist_controller import TodolistControllerPort, TODOLIST_CONTROLLER
from todolist_controller.presentation.todolist import TodolistPresentation


def start_app(dependencies: PyqureMemory):
    app = FastAPI()
    (_, inject) = pyqure(dependencies)

    @app.get("/todolist/{todolist_key}/task")
    def list_task(todolist_key) -> dict:
        controller: TodolistControllerPort = inject(TODOLIST_CONTROLLER)
        todolist = controller.get_todolist(UUID(todolist_key))
        tasks: list = get_tasks_or_default(todolist)
        return {"todolist": {
            "key": todolist_key,
            "tasks": tasks}}

    def get_tasks_or_default(todolist: TodolistPresentation | None) -> list[dict]:
        if todolist is None:
            return []
        return [{"key": str(task.key), "name": task.name, "is_opened": task.is_opened} for task in
                todolist.tasks]


    return app
