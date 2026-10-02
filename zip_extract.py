import zipfile
import traceback
from pathlib import Path

from path_mapping import PathMapping
from action_result import ActionResult

def guess_metadata_encoding(path, candidates=("cp437", "cp866", "cp1251", "gbk", "shift_jis")):
    with zipfile.ZipFile(path) as zf:
        raws = []
        for i in zf.infolist():
            if i.flag_bits & 0x800:
                continue
            try:
                raws.append(i.filename.encode("cp437"))
            except UnicodeEncodeError:
                raws.append(i.filename.encode("cp866", errors="replace"))

    if not raws:
        return None  # все имена в UTF-8, metadata_encoding не нужен
    blob = b"".join(raws)
    if all(b < 128 for b in blob):
        return None  # чистый ASCII
    try:
        blob.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    def score(enc):
        try:
            text = blob.decode(enc)
        except UnicodeDecodeError:
            return -1
        # для кириллицы: доля букв среди не-ASCII символов
        non_ascii = [c for c in text if ord(c) > 127]
        letters = sum(c.isalpha() for c in non_ascii)
        lower = sum(("а" <= c <= "я") or c in "ёЁ" for c in non_ascii)
        return (letters + lower) / max(len(non_ascii), 1)

    return max(candidates, key=score)

def _verify_extracted_contents(zfile: zipfile.ZipFile, extracted: list[tuple[zipfile.ZipInfo, str]]) -> bool:
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

def _all_extracted_paths_exist(extracted: list[tuple[zipfile.ZipInfo, str]]) -> bool:
    """Проверка существования извлеченного контента"""
    for _, ext_file_path in extracted:
        if not Path(ext_file_path).exists():
            return False
    return True

def _extract_archive(file_path: PathMapping, 
             dst_path: Path, 
             zip_filename_encoding = None,
             verify_extracted = True,) -> bool:
    """Непосредственная распаковка файлов из архива \n
     Возвращает статус: была распаковка и итог подтвержден 
    (в данном случае файлы существуют или верифицированы)"""
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

#main
def zip_extract(file_path: PathMapping, 
                zip_filename_encoding = None,
                verify_extracted = True,
                **kwargs) -> ActionResult:
    """Извлечение файлов из архива в ту же папку, 
    либо её копию в другом месте (с сохранением структуры дерева). \n
    zip_filename_encoding: может быть cp437, cp866, cp1251, utf-8 \n
    verify_extracted: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве \n
    Возвращает статус: были изменения и итог подтвержден 
    (в данном случае файлы существуют или верифицированы)"""

    dst_path = file_path.dst_path.parent
    if not zip_filename_encoding:
        try:
            zip_filename_encoding = guess_metadata_encoding(file_path)
            if zip_filename_encoding:
                print(f"[INFO] в архиве {file_path} определена/угадана кодировка: {zip_filename_encoding}")
        except Exception:
            print(f"[WARNING] не удалось определить/угадать кодировку в архиве {file_path}")
    extract_confirmed  = _extract_archive(file_path = file_path,
                                dst_path = dst_path,
                                zip_filename_encoding = zip_filename_encoding,
                                verify_extracted = verify_extracted)

    return ActionResult(change_confirmed=extract_confirmed, 
            safe_to_remove_source=verify_extracted and extract_confirmed and not file_path.need_copy_to_dst)


# NOTE: не зип файлы не переносятся: если нужна копия не зип файла, 
# то replace_in_name делает это, даже если изменений не было произведено
