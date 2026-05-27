from common import PathMapping, ActionResult, walk_and_edit
from replace_in_name import apply_name_replacements
from zip_and_file_rename import rename_single_root_to_archive_name

def two_renames(file_path: PathMapping,
                find_what: list[str],
                replace_with: str = "",
                **kwargs) -> ActionResult:
    """"""
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
        action_func = two_renames, 
        output_dir = output_dir,
        need_copy = need_copy,
        accept_file_ext_to_change = accept_file_ext_to_change,
        func_kwargs = dict(find_what = find_what_replaced,
                       replace_with = replace_with),
        )

def main():
    input_dir = "D:\\Книги\\_update"
    output_dir = "D:\\Книги\\_update2"
    accept_file_ext_to_change = [".fb2", ".zip"]
    find_what_replaced = [".fb2", ".epub"]
    replace_with = ""

    run(
        input_dir = input_dir,
        output_dir = output_dir,
        # need_copy = False,
        accept_file_ext_to_change = accept_file_ext_to_change,

        find_what_replaced = find_what_replaced,
        replace_with = replace_with,
        )

if __name__  == '__main__':
    main()