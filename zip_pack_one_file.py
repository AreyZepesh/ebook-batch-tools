from common import (
    zipfile, traceback, Path,
    PathMapping,
    walk_and_edit, 
        )

def _verify_packed_file(zip_path: Path, src_file: PathMapping) -> bool:
    # верификация
    with zipfile.ZipFile(zip_path, 'r') as zfile:
        members_list = zfile.infolist()
        if len(members_list) != 1:
            print(f"Больше одного файла в архиве: {zip_path}")
            return False
        
        member = members_list[0]
        content = zfile.read(member)
        with open(src_file, 'rb') as file:
            if content != file.read():
                print(f'! Ошибка: {member.filename} >>> {src_file}')
                return False
    return True

def pack_to_zip(file_path: PathMapping,
                verify_packed = False,
                **kwargs):
    
    # Порядок важен, если сперва сохранить в переменную, 
    # а потом менять - не будет проверки на дубль названия
    # file_path.dst_path = dst_path.with_name(dst_path.name + ".zip")
    file_path.dst_path = file_path.dst_path.with_suffix(".zip")
    dst_path: Path = file_path.dst_path
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(dst_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            print(f"Пишем: {dst_path}")
            zip_file.write(filename = file_path, arcname = file_path.name)

    except Exception as ex:
        print(f"ERROR: какая то ошибка при работе с: {file_path}")
        print(f"{traceback.format_exc()}")
        return

    print(f"Успешно запаковано: {file_path} >>> {dst_path}")
    if verify_packed:
        is_verefy = _verify_packed_file(dst_path, file_path)
        print(f"   Результат верефикации: {is_verefy}")

def run(input_dir: str, 
        output_dir: str = None,
        need_copy: bool = True,
        accept_file_ext_to_change: list = [".fb2"],
        verify_packed = False,
            ) -> None:
    """Запуск основной функции модуля"""
    walk_and_edit(
        input_dir = input_dir, 
        action_func = pack_to_zip, 
        output_dir = output_dir,
        need_copy = need_copy,
        accept_file_ext_to_change = accept_file_ext_to_change,
        func_kwargs = dict(verify_packed = verify_packed),
        )

def main():
    input_dir = "D:\\Книги\\_update"
    output_dir = "D:\\Книги\\_update2"
    accept_file_ext_to_change = [".fb2"]

    run(
        input_dir = input_dir, 
        output_dir = output_dir,
        # need_copy = False,
        accept_file_ext_to_change = accept_file_ext_to_change,
        verify_packed = True
        )

if __name__  == '__main__':
    main()