from common import PathMapping, ActionResult, walk_and_edit
from replace_in_name import apply_name_replacements
from zip_rename_root import rename_single_root_to_archive_name

def rename_and_sync_root(file_path: PathMapping,
                find_what: list[str],
                replace_with: str = "",
                **kwargs) -> ActionResult:
    """Сперва меняем имя архива, после и имя файла/папки в нем, сохраняем"""
    # Переименовываем файл, если нужно
    apply_name_replacements(file_path=file_path, find_what=find_what, replace_with=replace_with)

    return rename_single_root_to_archive_name(file_path)

def run(input_dir: str, 
        output_dir: str = None,
        need_copy: bool = True,
        accept_file_ext_to_change: list = [".zip"], 

        find_what_replaced: list[str] = [".fb2"], 
        replace_with: str = "", 
            ) -> None:
    """Запуск основной функции модуля"""
    walk_and_edit(
        input_dir = input_dir, 
        action_func = rename_and_sync_root, 
        output_dir = output_dir,
        need_copy = need_copy,
        accept_file_ext_to_change = accept_file_ext_to_change,
        func_kwargs = dict(find_what = find_what_replaced,
                       replace_with = replace_with),
        )

