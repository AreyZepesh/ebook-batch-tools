from common import (
    os, zipfile, traceback, tempfile,
    Path, PathMapping,
    walk_and_edit, 
        )

def rename_single_root_to_archive_name(file_path: PathMapping, 
                                       **kwargs):
    # TODO разделить логику? 
    # отдельную функцию когда только один файл, и отдельную для папки? 
    # хотя зачем? 
    # FIXME 1 думаю надо будет вынести просто все действия с архивами в ФС в другую функцию выше, 
    # а открытие архивов функцией ниже
    # TODO если весть log для реверсивной обработки:
    # в лог изменений сохранять (src_path, изначальное_корневое_имя, новое_корневое_имя, dst_path)
    
    # Создаем временный архив 
    tmp_fd, temp_path = tempfile.mkstemp(
        prefix="tmp_",
        suffix=".zip",
        dir=file_path.parent,  
        # NOTE ? сейчас делает в исходной папке, а надо наверно в целевой
        # важно: та же ФС для атомарного replace  - говорил ии
            )
    os.close(tmp_fd)  # ZipFile сам откроет путь
    temp_path = PathMapping(temp_path)

    try:
        # Открываем исходный файл
        with zipfile.ZipFile(file_path, "r") as zip_read:
            # Получаем список всего в архиве
            namelist = [name.replace("\\", "/") for name in zip_read.namelist()]
            # Делаем сет для контроля количества элементов в корне 
            # отрабатываются только архивы с одной папкой или файлом 
            # изначально функция разрабатывалось только под один файл, но выросла... а надо ли? !???!
            root_items = {
                    name.split("/", 1)[0]
                    for name in namelist
                    if name.strip("/")
                        }
            
            if len(root_items) != 1:
                # Если в корне больше одного элемента - возращаем ощибку и завершаем функцию
                print(f"Больше одного файла/папки в корне: {file_path}")
                return
            
            # эээ... чет я уже не помню, зачем такая конструкция
            # достаем элемент из set, возможно явнее будет через pop?
            root_item = next(iter(root_items))
            # Делим корневой элемент на имя и расширение
            root_stem, root_suffix = os.path.splitext(root_item)
            
            # Если "Имя файла/папки в корне идентично имени архива" - завершаем функцию
            if root_stem == file_path.stem:
                print(f"Имя файла/папки в корне идентично имени архива: {file_path}")
                # print(f"{traceback.format_exc()}")
                
                # TODO переносить файл, в целевую папку... отдельной переменной T/F?
                # FIXME 1 нельзя переместить, так как файл открыт (мы в with)
                # dst_path = file_path.transfer()
                return # (str(file_path), str(dst_path))
            
            print(f"{file_path}:")
            # Открываем временный файл
            with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_write:
                # обходим элементы исходного архива, и подменяем им корневое имя
                for item in zip_read.infolist():
                    old_path = item.filename
                    if old_path == root_item:
                        # обновляем имя корневого файла на имя архива, сохраняя суффикс
                        new_path = file_path.stem + root_suffix
                    elif old_path.startswith(root_item + "/") or old_path.startswith(root_item + "\\"):
                        # обновляем имя корневой папки на имя архива
                        new_path = file_path.stem + old_path[len(root_item):]
                        # new_path = file_path.stem + root_ext + old_path[len(root_item):]
                    else:
                        # теоретически не должно случиться, оставляем как было
                        new_path = old_path  
                    # new_path = item.filename.replace(root_name, file_path.stem, 1),

                    print(f"    {item.filename} >>> {new_path}")
                    # копируем zip метаданные, или как их там? сжатие и прочее
                    data = zip_read.read(item.filename)
                    # меняем путь к файлу до нового
                    item.filename = new_path

                    # пишем файл и данные во временный архив
                    zip_write.writestr(zinfo_or_arcname = item, data = data)

        # Кэшируем
        dst_path: Path = file_path.dst_path
        # создаем папку, если её нет
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        # переносим временный файл в конечную точку 
        temp_path.replace(dst_path)
        print(f"        >>> {dst_path}")

        # Если не нужна была исходная копия - удаляем оригинал
        if file_path.should_delete_source():
            print("REMOVE")
            os.remove(file_path)

    except zipfile.BadZipFile:
        print(f"ERROR: Битый архив, пропускаем: {file_path}")
    except Exception as ex:
        print(f"ERROR: какая то ошибка с архивом: {file_path}")
        print(traceback.format_exc())
    finally:
        # удаляем временный файл, если он вдруг остался в системе
        if os.path.exists(temp_path):
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
