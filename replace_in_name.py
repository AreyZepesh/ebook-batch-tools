from path_mapping import PathMapping
from action_result import ActionResult

from logger import setup_logging, q
logger = setup_logging()

def apply_name_replacements(
    file_path: PathMapping,
    find_what: tuple[str]|list[str],
    replace_with: str = ""):
    """Заменяем искомое в пути \n
    Apply configured stem replacements to dst_path."""
    matched = False
    # обходим по одной строки, которые нужно заменить
    for find_str in find_what:
        # проверка наличия такой строки
        if find_str in file_path.stem:
            matched = True
            # заменяем слова в конечном пути
            logger.debug("Замена в названии файла %s: %s на %s" % (q(file_path), find_str, replace_with))
            file_path.replace_in_dst_stem(find_str, replace_with)
    return matched

#main
def rename_file(
        file_path: PathMapping, 
        find_what: tuple[str]|list[str], 
        replace_with: str = "",  
        **kwargs) -> ActionResult:
    """Переименовывает файл, заменяя одно на другое, \n
    Например: 'Книга.fb2.zip' станет 'Книга.zip' \n
    file_path: путь к архиву \n
    find_what: список, что изменить \n
    replace_with: строка, на которую заменяется\n
    Возвращает статус: были изменения и итог подтвержден (в данном случае файлы существуют)"""
    rename_confirmed = False

    apply_name_replacements(file_path=file_path, find_what=find_what, replace_with=replace_with)

    # NOTE это немного спорное, но осмысленное решение: 
    # если вдруг по какой то неясной причине кому то нужна будет 
    # копия файла без изменений - он её получит
    dst_path = file_path.dst_path
    if file_path.should_transfer():
        dst_path = file_path.transfer()
        logger.info("Создание файла с новым именем: %s >>> %s" % (q(file_path), q(dst_path)))
        rename_confirmed = dst_path.exists()

    return ActionResult(change_confirmed=rename_confirmed, 
                        safe_to_remove_source=file_path.should_delete_source())
