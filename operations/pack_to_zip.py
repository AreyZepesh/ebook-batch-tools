import zipfile
import traceback
from pathlib import Path

from core.path_mapping import PathMapping
from core.action_result import ActionResult

from core.logger import setup_logging, q
logger = setup_logging()

def _verify_packed_file(zip_path: Path, src_file: PathMapping) -> bool:
    # верификация
    with zipfile.ZipFile(zip_path, 'r') as zfile:
        members_list = zfile.infolist()
        if len(members_list) != 1:
            logger.warning("Верефикация упакованного файла провалена: больше одного файла в архиве: %s", q(zip_path) )
            return False
        
        member = members_list[0]
        content = zfile.read(member)
        with open(src_file, 'rb') as file:
            if content != file.read():
                logger.warning("Верефикация упакованного файла провалена: несоответствие: %s >>> %s", q(member.filename), q(src_file) )
                return False
    logger.debug("Верефикация прошла успешно: %s ", q(zip_path))
    return True

def _pack_archive(file_path: PathMapping, 
             dst_path: Path, 
             verify_packed = False,) -> bool:
    """Непосредственная упаковка файла в архив \n
     Возвращает статус: была упаковка и итог подтвержден 
    (в данном случае файлы существуют или верифицированы)"""
    try:
        with zipfile.ZipFile(dst_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            logger.debug("Упаковываем в архив: %s", q(dst_path))
            zip_file.write(filename = file_path, arcname = file_path.name)

    except Exception:
        logger.warning("ERROR: какая то ошибка при упаковке: %s в %s \n%s", q(file_path), q(dst_path), traceback.format_exc() )
        return False

    if verify_packed:
        return _verify_packed_file(dst_path, file_path)
    return dst_path.exists()

#main
def pack_to_zip(file_path: PathMapping,
                verify_packed = False,
                save_suffix_in_name = False,
                **kwargs) -> ActionResult:
    """Создание архива на основе одного файла в ту же папку, 
    либо в другом месте (с сохранением структуры дерева). \n
    verify_packed: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве \n
    save_suffix_in_name: Если нужно сохранить расширение архивированного файла в имени архива\n
    Возвращает статус: были изменения и итог подтвержден 
    (в данном случае файлы существуют или верифицированы)"""
    # Порядок важен, если сперва сохранить в переменную, 
    # а потом менять - не будет проверки на дубль названия
    if save_suffix_in_name:
        file_path.set_dst_stem(file_path.name)
    file_path.set_dst_suffix(".zip")

    dst_path: Path = file_path.dst_path
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    pack_confirmed = _pack_archive(file_path = file_path,
                                dst_path = dst_path,
                                verify_packed = verify_packed)
    
    if pack_confirmed:
        logger.info("Успешно запаковано: %s >>> %s", q(file_path), q(dst_path) )

    return ActionResult(change_confirmed=pack_confirmed, safe_to_remove_source=file_path.should_delete_source())

