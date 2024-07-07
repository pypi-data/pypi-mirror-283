from abc import ABC, abstractmethod
from typing import Callable, NoReturn, TypeVar


Task = Callable  # Any callable is a valid Task
Task_T = TypeVar("Task_T", bound=Task)


class Application(ABC):
    @abstractmethod
    def register(self) -> Callable[[Task_T], Task_T]: ...

    @abstractmethod
    def __call__(self) -> NoReturn:
        # usage: app = XXApplication()
        # ... (register your task)
        # app()
        ...
