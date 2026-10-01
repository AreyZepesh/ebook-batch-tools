from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable, TYPE_CHECKING

from path_mapping import PathMapping
from action_result import ActionResult

@dataclass
class Action:
    """Что выполнять на каждом подходящем файле — функция и её аргументы вместе."""
    func: Callable[..., ActionResult]
    accept_ext: list[str]
    kwargs: dict = field(default_factory=dict)

    def __call__(self, file_path: PathMapping) -> ActionResult:
        return self.func(file_path=file_path, **self.kwargs)

@dataclass
class Config:
    input_dir: PathMapping
    output_dir: PathMapping | None = field(default=None)
    need_copy: bool = field(default=True)
    action: Action | None = field(default=None)

    def __setattr__(self, name, value):
        if name == 'input_dir':
            if value is None:
                raise ValueError("Не указан путь до начальной директории")
            value = PathMapping(value).resolve()
            if not value.exists():
                raise ValueError("Путь до начальной директории не существует")
            if not value.is_dir():
                raise ValueError("Путь до начальной директории — не папка")
        if name == 'output_dir':
            if value is not None:
                value = PathMapping(value).resolve()
        super().__setattr__(name, value)


