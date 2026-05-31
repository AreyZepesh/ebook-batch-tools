from common import (
    zipfile, traceback,
    Path, PathMapping, ActionResult,
    walk_and_edit, 
        )

def _verify_extracted_contents(zfile: zipfile.ZipFile, extracted: list[tuple[str]]) -> bool:
    """Верификация содержимого извлеченного контента"""
    for member, ext_path in extracted:
        if member.is_dir():
            continue

        content = zfile.read(member)
        with open(ext_path, 'rb') as file:
            if content != file.read():
                print(f'! Ошибка: {member.filename} >>> {ext_path}')
                return False
    return True

def _all_extracted_paths_exist(extracted: list[tuple[str]]) -> bool:
    """Проверка существования извлеченного контента"""
    for _, ext_file_path in extracted:
        if not Path(ext_file_path).exists():
            return False
    return True

def _extract_archive(file_path: PathMapping, 
             dst_path: Path|PathMapping, 
             zip_filename_encoding = None,
             verify_extracted = True,) -> bool:
    """Непосредственная распаковка файлов из архива \n
     Возвращает статус: была распаковка и итог подтвержден 
    (в данном случае файлы существуют или верефицированны)"""
    extracted = []
    try:
        with zipfile.ZipFile(file_path, 'r',
                             metadata_encoding=zip_filename_encoding,
                            ) as zfile:
            print(f"Извлечено из: {file_path}")
            # print(f" в {dst_path}")

            for member in zfile.infolist():
                ext_path = zfile.extract(member, dst_path)
                extracted.append( (member, ext_path) )
                print(f"  {member.filename} >>> {ext_path}")

            if verify_extracted:
                return _verify_extracted_contents(zfile, extracted)
            return _all_extracted_paths_exist(extracted)

    except zipfile.BadZipFile:
        print(f"ERROR: Битый архив, пропускаем: {file_path}")
        return False
    except Exception as ex:
        print(f"ERROR: какая то ошибка при работе с архивом: {file_path}")
        print(f"{traceback.format_exc()}")
        return False

def zip_extract(file_path: PathMapping, 
                zip_filename_encoding = None,
                verify_extracted = True,
                **kwargs) -> ActionResult:
    """Извлечение файлов из архива в ту же папку, 
    либо её копию в другом месте (с сохранением структуры дерева). \n
    zip_filename_encoding: может быть cp437, cp866, cp1251, utf-8 \n
    verify_extracted: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве \n
    Возвращает статус: были изменения и итог подтвержден 
    (в данном случае файлы существуют или верефицированны)"""

    dst_path = file_path.dst_path.parent
    extract_confirmed  = _extract_archive(file_path = file_path,
                                dst_path = dst_path,
                                zip_filename_encoding = zip_filename_encoding,
                                verify_extracted = verify_extracted)

    return ActionResult(change_confirmed=extract_confirmed, 
            safe_to_remove_source=verify_extracted and extract_confirmed and not file_path.need_copy_to_dst)

def run(input_dir: str, 
        output_dir: str = None,
        need_copy: bool = True,
        accept_file_ext_to_change: list = [".zip"], 

        zip_filename_encoding=None,
        verify_extracted=True,
            ) -> None:
    """Запуск основной функции модуля"""
    walk_and_edit(
        input_dir = input_dir, 
        action_func = zip_extract, 
        output_dir = output_dir,
        need_copy = need_copy,
        accept_file_ext_to_change = accept_file_ext_to_change,
        func_kwargs = dict(zip_filename_encoding = zip_filename_encoding,
                           verify_extracted = verify_extracted ),
        )

def main():
    input_dir = "D:\\Книги\\_update"
    output_dir = "D:\\Книги\\_update2"
    # input_dir = "D:\\Книги\\По новому (выборка) (2026-05-27)"
    # output_dir = "I:\\Книги\\"
    accept_file_ext_to_change = [".zip"]

    run(
        input_dir = input_dir, 
        output_dir = output_dir,
        # need_copy = False,
        accept_file_ext_to_change = accept_file_ext_to_change,

        zip_filename_encoding = "cp866",
        # verify_extracted = False
        )

if __name__  == '__main__':
    main()

# NOTE: не зип файлы не переносятся
# TODO: копировать не архивы с указанными расширениями?