from path_mapping import PathMapping
from action_result import ActionResult
from replace_in_name import apply_name_replacements
from zip_rename_root import rename_single_root_to_archive_name

#main
def rename_and_sync_root(file_path: PathMapping,
                find_what: tuple[str]|list[str],
                replace_with: str = "",
                **kwargs) -> ActionResult:
    """Сперва меняем имя архива, после и имя файла/папки в нем, сохраняем"""
    # Переименовываем файл, если нужно
    apply_name_replacements(file_path=file_path, find_what=find_what, replace_with=replace_with)

    return rename_single_root_to_archive_name(file_path)
