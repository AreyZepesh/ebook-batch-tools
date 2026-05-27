from common import (
    os, zipfile, traceback, tempfile,
    Path, PathMapping, ActionResult,
    walk_and_edit, 
        )

def _create_temp_zip_near(file_path: PathMapping) -> PathMapping:
    """Создаем временный архив""" 
    tmp_fd, temp_path = tempfile.mkstemp(
        prefix="tmp_",
        suffix=".zip",
        dir=file_path.parent,  
        # NOTE ? сейчас делает в исходной папке, а надо наверно в целевой
        # важно: та же ФС для атомарного replace  - говорил ии
            )
    os.close(tmp_fd)  # ZipFile сам откроет путь
    return PathMapping(temp_path)

def _get_single_root_item(zip_read: zipfile.ZipFile) -> str | None:
    """Получаем корневой элемент в архиве, если больше одного - None"""
    namelist = [name.replace("\\", "/") for name in zip_read.namelist()]
    root_items = {
            name.split("/", 1)[0]
            for name in namelist
            if name.strip("/")
                }
    
    if len(root_items) != 1:
        return None
    
    return root_items.pop()

def _build_renamed_member_path(old_path: str, root_item: str, archive_stem: str, root_suffix: str) -> str:
    """Переименовываем только корневой (высокоуровневый) элемент в архиве.
    \nRename only the top-level root item inside archive."""
    if old_path == root_item:
        # обновляем имя корневого файла на имя архива, сохраняя суффикс
        return archive_stem + root_suffix
    elif old_path.startswith(root_item + "/") or old_path.startswith(root_item + "\\"):
        # обновляем имя корневой папки на имя архива
        return archive_stem + old_path[len(root_item):]
    # теоретически не должно случиться, оставляем как было
    return old_path  

def _rewrite_archive(
    zip_read: zipfile.ZipFile,
    temp_path: PathMapping,
    archive_stem: str,
    root_item: str,
    root_suffix: str,
                ):
    """Записываем файлы во временный архив"""
    # Открываем временный файл
    with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_write:
        # обходим элементы исходного архива, и подменяем им корневое имя
        for item in zip_read.infolist():
            old_path = item.filename
            new_path = _build_renamed_member_path(old_path, root_item, archive_stem, root_suffix)
            print(f"    {item.filename} >>> {new_path}")
            # копируем zip метаданные, или как их там? сжатие и прочее
            data = zip_read.read(item.filename)
            # меняем путь к файлу до нового
            item.filename = new_path
            # пишем файл и данные во временный архив
            zip_write.writestr(zinfo_or_arcname = item, data = data)

def _prepare_renamed_archive(file_path: PathMapping) -> None|PathMapping|Path:
    """Непосредственная работа с архивом \n
     Возвращает путь: что именно переместить в конечную точку"""
    target_archive_stem = file_path.stem
    if file_path.dst_stem_changed():
        target_archive_stem = file_path.get_dst_stem()
    # Открываем исходный файл
    with zipfile.ZipFile(file_path, "r") as zip_read:
        print(f"\n{file_path}:")
        root_item = _get_single_root_item(zip_read)
        if root_item is None:
            # Если в корне больше одного элемента - возращаем ощибку и завершаем функцию
            print(f"   Больше одного файла/папки в корне")
            return None
        
        # Делим корневой элемент на имя и расширение
        root_stem, root_suffix = os.path.splitext(root_item)
        
        # Если "Имя файла/папки в корне идентично имени архива" - завершаем функцию
        if root_stem == target_archive_stem:
            print(f"   Имя файла/папки в корне идентично конечному имени архива: {target_archive_stem}")
            return file_path
        
        temp_path = _create_temp_zip_near(file_path)

        _rewrite_archive(
                    zip_read=zip_read,
                    temp_path=temp_path,
                    archive_stem=target_archive_stem,
                    root_item=root_item,
                    root_suffix=root_suffix,
                        )
        return temp_path


def rename_single_root_to_archive_name(file_path: PathMapping, **kwargs) -> ActionResult:
    """
    """
    
    temp_path = None
    action_result = ActionResult()
    try:
        temp_path = _prepare_renamed_archive(file_path)
        if temp_path is None:
            return ActionResult()

        # Кэшируем
        dst_path: Path = file_path.dst_path
        same_pathes = file_path.src_is_same(temp_path)

        if same_pathes and file_path.should_transfer():
            dst_path: Path = file_path.transfer()
            action_result.change_confirmed = dst_path.exists()

        if not same_pathes:
            # создаем папку, если её нет
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            # переносим временный файл в конечную точку 
            temp_path.replace(dst_path)
            action_result.change_confirmed = dst_path.exists()

        if action_result.change_confirmed:
            print(f"        >>> {dst_path}")
            action_result.safe_to_remove_source = file_path.should_delete_source()
        return action_result
    except zipfile.BadZipFile:
        print(f"ERROR: Битый архив, пропускаем: {file_path}")
        return ActionResult()
    except Exception as ex:
        print(f"ERROR: какая то ошибка с архивом: {file_path}")
        print(traceback.format_exc())
        return ActionResult()
    finally:
        # удаляем временный файл, если он вдруг остался в системе
        if temp_path and os.path.exists(temp_path):
            if not file_path.src_is_same(temp_path):
                    os.remove(temp_path)
        


def run(input_dir: str, 
        output_dir: str = None,
        need_copy: bool = True,
        accept_file_ext_to_change: list = [".zip"], 
            ) -> None:
    """Запуск основной функции модуля"""
    walk_and_edit(
        input_dir = input_dir, 
        action_func = rename_single_root_to_archive_name, 
        output_dir = output_dir,
        need_copy = need_copy,
        accept_file_ext_to_change = accept_file_ext_to_change,
        # func_kwargs = dict(),
        )

def main():
    input_dir = "D:\\Книги\\_update"
    output_dir = "D:\\Книги\\_update2"
    accept_file_ext_to_change = [".zip"]

    run(
        input_dir = input_dir, 
        output_dir = output_dir,
        # need_copy = False,
        accept_file_ext_to_change = accept_file_ext_to_change,
        )

if __name__  == '__main__':
    main()
