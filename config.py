from pathlib import Path
from path_mapping import PathMapping
from walker import ActionResult, walk_and_edit
from dataclasses import dataclass, field
from typing import Callable

@dataclass
class Action:
    """Что выполнять на каждом подходящем файле — функция и её аргументы вместе."""
    func: Callable[..., ActionResult]
    accept_ext: list[str]
    kwargs: dict = field(default_factory=dict)

@dataclass
class Config:
    input_dir: str | Path | PathMapping
    output_dir: str | Path | PathMapping | None = None
    need_copy: bool = field(default=True)
    action: Action | None = None

    def __setattr__(self, name, value):
        if name == 'input_dir':
            if value is None or value == "..":
                raise ValueError("Не указан путь до начальной директории")
            value = PathMapping(value).resolve()
            if not value.exists():
                raise ValueError("Путь до начальной директории не существует")
        if name == 'output_dir':
            if value is not None:
                value = PathMapping(value).resolve()
        super().__setattr__(name, value)


c = Config(input_dir = ".1")
print(c.__dict__)