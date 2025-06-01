import os

from dotenv import load_dotenv
from pyqure import PyqureMemory, pyqure
from todolist_controller import injection_keys as keys
from todolist_controller import provide_todolist_controller

from todolist_back.app import start_app


def provide_dependencies() -> PyqureMemory:
    dependencies: PyqureMemory = {}
    (provide, _) = pyqure(dependencies)
    load_dotenv()
    provide(keys.TODOLIST_DB_NAME, os.getenv("DB_NAME"))
    provide(keys.TODOLIST_DB_USER, os.getenv("DB_USER"))
    provide(keys.TODOLIST_DB_PASSWORD, os.getenv("DB_PASSWORD"))
    provide(keys.TODOLIST_DB_HOST, os.getenv("DB_HOST"))
    provide(keys.TODOLIST_DB_PORT, int(os.getenv("DB_PORT", "0")))

    provide_todolist_controller(dependencies)

    return dependencies


app = start_app(provide_dependencies())
