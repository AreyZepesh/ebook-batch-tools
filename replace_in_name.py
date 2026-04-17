from common import (
    # os, zipfile, traceback, tempfile,
    PathMapping,
    walk_and_edit, 
        )

def rename_file(
        file_path: PathMapping, 
        find_what: list[str], 
        replace_with: str = "",  
        **kwargs): # -> tuple[str]:
    """Переименовывает файл, заменяя одно на другое, \n
    Например: 'Книга.fb2.zip' станет 'Книга.zip' \n
    file_path: путь к архиву \n
    find_what: список, что изменить \n
    replace_with: строка, на которую заменяется\n"""
    # обходим по одной строки, которые нужно заменить
    for find_str in find_what:
        # проверка наличия такой строки
        if find_str in file_path.stem:
            # заменяем слова в конечном пути
            file_path.replace_in_dst_stem(find_str, replace_with)

    dst_path = file_path.transfer()

    print(f"{file_path} >>> {dst_path}")
    # return (str(file_path), str(dst_path))

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
        action_func = rename_file, 
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
        # output_dir = output_dir,
        need_copy = False,
        accept_file_ext_to_change = accept_file_ext_to_change,

        find_what_replaced = find_what_replaced,
        replace_with = replace_with,
        )

if __name__  == '__main__':
    main()