from common import (
    zipfile, traceback,
    PathMapping,
    walk_and_edit, 
        )

def _verify_extracted_file(zfile: zipfile.ZipFile, extracted: list[tuple[str]]) -> bool:
    # верификация
    for member, ext_path in extracted:
        if member.is_dir():
            continue

        content = zfile.read(member)
        with open(ext_path, 'rb') as file:
            if content != file.read():
                print(f'! Ошибка: {member.filename} >>> {ext_path}')
                return False
    return True

def zip_extract(file_path: PathMapping, 
                zip_filename_encoding = None,
                verify_extracted = False,
                **kwargs):
    """извлекает архивы в ту же папку, либо её копию в другом месте. \n
    zip_filename_encoding: может быть cp437, cp866, cp1251, utf-8 \n
    verify_extracted: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве """
    dst_path = file_path.dst_path.parent
    # may_delete = False 
    try:
        with zipfile.ZipFile(file_path, 'r',
                             metadata_encoding=zip_filename_encoding,
                            ) as zfile:
            print(f"Извлечено из: {file_path}")
            print(f" в {dst_path}")

            # zfile.extractall(dst_path)
            extracted = []
            for member in zfile.infolist():
                ext_path = zfile.extract(member, dst_path)
                extracted.append( (member, ext_path) )
                print(f"  {member.filename} >>> {ext_path}")

            if verify_extracted:# or not file_path.need_copy_to_dst:
                # may_delete = _verify_extracted_file(zfile, extracted)
                _verify_extracted_file(zfile, extracted)

    except zipfile.BadZipFile:
        print(f"ERROR: Битый архив, пропускаем: {file_path}")
        # may_delete = False
    except Exception as ex:
        print(f"ERROR: какая то ошибка при работе с архивом: {file_path}")
        print(f"{traceback.format_exc()}")
        # may_delete = False
    
    # if not file_path.need_copy_to_dst and may_delete:
    #     # удаление оригинала только если не нужна копия и прошла верефикация
    #     print(f"Файл удален: {file_path}")
    #     os.remove(file_path)

def run(input_dir: str, 
        output_dir: str = None,
        need_copy: bool = True,
        accept_file_ext_to_change: list = [".zip"], 

        zip_filename_encoding=None,
        verify_extracted=False,
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
    accept_file_ext_to_change = [".zip"]

    run(
        input_dir = input_dir, 
        output_dir = output_dir,
        need_copy = False,
        accept_file_ext_to_change = accept_file_ext_to_change,

        zip_filename_encoding = "cp866",
        verify_extracted = False
        )

if __name__  == '__main__':
    main()