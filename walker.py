from config import Config
from path_mapping import PathMapping
from action_result import ActionResult

def walk_and_edit(config: Config) -> None:
    if config.action is None:
        raise ValueError("config.action обязателен")
    
    accept_ext = {ext.lower() for ext in config.action.accept_ext}
    file_list: list[PathMapping] = list(config.input_dir.glob("**/*"))

    for file_path in file_list:
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in accept_ext:
            continue
        if config.output_dir:
            file_path.remap_dst_path(config.input_dir, config.output_dir)
        file_path.need_copy_to_dst = config.need_copy

        try:
            action_result: ActionResult = config.action(file_path)
        except Exception as ex:
            # NOTE: FIXME: Общая затычка ошибок, чтоб одна ошибка не руинила цикл
            print(f"[ERROR] {file_path}) ")
            print("     ", ex)
            continue
        
        if not isinstance(action_result, ActionResult):
            raise TypeError(f"Функция {config.action.func.__name__} вернула неожиданный результат или None")
        
        if action_result.can_remove_source(): # and not need_copy:
            file_path.remove()
            print(f"!   Удален исходный файл: {file_path}")