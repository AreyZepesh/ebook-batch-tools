from pathlib import Path
from dataclasses import dataclass, field

from path_mapping import PathMapping
@dataclass
class ActionResult():
    change_confirmed: bool = field(default=False)
    safe_to_remove_source: bool = field(default=False)

    def can_remove_source(self):
        return self.change_confirmed and self.safe_to_remove_source


def walk_and_edit(
        input_dir: str | Path, 
        output_dir: str | Path | None = None, 
        need_copy: bool = True,
        accept_file_ext_to_change: list = [".zip"],

        action_func = None, 
        func_kwargs: dict = None,
            ) -> None:
    if action_func is None:
        raise ValueError("action_func обязателен")
    accept_ext = {ext.lower() for ext in accept_file_ext_to_change}
    file_list = list(PathMapping(input_dir).glob("**/*"))
    for file_path in file_list:
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in accept_ext:
            continue
        if output_dir:
            file_path.remap_dst_path(input_dir, output_dir)

        file_path.need_copy_to_dst = need_copy

        try:
            action_result: ActionResult = action_func(file_path = file_path,
                                **func_kwargs or {})
        except Exception as ex:
            # NOTE: FIXME: Общая затычка ошибок, чтоб одна ошибка не руинила цикл
            print(f"[ERROR] {file_path}) ")
            print(ex)
            continue
        
        if not isinstance(action_result, ActionResult):
            raise Exception(f"Функция {action_func.__name__} вернула None")
        
        if action_result.can_remove_source(): # and not need_copy:
            file_path.remove()
            print(f"!   Удален исходный файл: {file_path}")
        

