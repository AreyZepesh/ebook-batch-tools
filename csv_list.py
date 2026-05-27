from common import (
    os, zipfile, traceback, tempfile,
    PathMapping, ActionResult, Path, 
    dataclass, field,
        )
import csv


class FileInfo():
    all_filenames = []
    max_parts_in_path = 0
    need_tag_dublicates: bool = True

    def __init__(self, path_parts: tuple[str], filename: str, ):
        self.path_parts = path_parts
        self.filename = filename
        self.is_dublicate = False

        self._class_var_update()

    def _class_var_update(self):
        if self.filename not in type(self).all_filenames:
            type(self).all_filenames.append(self.filename)
        else:
            self.is_dublicate = True

        type(self).max_parts_in_path = max(len(self.path_parts), type(self).max_parts_in_path)

    def get_as_tuple_from_csv(self, space_before: bool = False, first_part_in_first_space: bool = False) -> tuple[str]:
        """Возвращает tuple для формирования строки в csv. \n
        Добавляет пустые ячейки в промежутки до частей пути или после, но до имени файла. \n
        space_before: будут ли пустые ячейки до частей пути, или нет. Иначе - после, но до имени файла \n
        first_part_in_first_space: работает только при space_before = True. Переносит первую часть пути в первую пустую ячейку. """
        ratio = type(self).max_parts_in_path - len(self.path_parts)
        path_parts = self.path_parts
        # print(f"{ratio=} {self.path_parts=}")
        if space_before:
            self.path_parts = ('',)*ratio + path_parts
            if first_part_in_first_space:
                self.path_parts = (path_parts[0],) + ('',)*ratio + tuple(path_parts[1:])
                # print(f"   {ratio=} {self.path_parts=}")
                # import time
                # time.sleep(10)
        else:
            self.path_parts = path_parts + ('',)*ratio

        tag = tuple()
        if type(self).need_tag_dublicates:
            tag += (self.is_dublicate if self.is_dublicate else "",)
        return self.path_parts + (self.filename,) + tag

    @classmethod
    def _get_csv_header(cls):
        tag = tuple()
        if cls.need_tag_dublicates:
            tag += ('is_dublicate',)

        if cls.max_parts_in_path >= 1:
            return ('folder',) + ('subfolder',)*(cls.max_parts_in_path-1) + ('filename',) + tag
        else:
            return  ('filename',) + tag
         



def main():
    input_dir = "D:\\Книги\\_update"
    input_dir = "D:\\Книги\\По новому (выборка) (2026-04-21)"

    if os.path.exists("./list.csv"):
        os.remove("./list.csv")

    items = []

    
    
    for dirpath, _, filenames in Path(input_dir).walk():
        for filename in filenames:
            items.append(FileInfo(dirpath.relative_to(input_dir).parts, filename))

    # for item in items:
    #     print(item)

    # FileInfo.need_tag_dublicates = False

    with open("./list.csv", "a", 
            #   encoding="utf8"
              encoding="cp1251"
              ) as file:
        csv_out = csv.writer(file, delimiter=";", lineterminator="\n")
        
        csv_out.writerow(FileInfo._get_csv_header())
        for item in items:
            item: FileInfo = item
            csv_out.writerow( item.get_as_tuple_from_csv(
                # space_before = True, 
                # first_part_in_first_space = True,
                ) )

# ок, просто список с выравниванием по правому краю работает
# что еще хотел?
#+ метку дубликата, по имени файла 
#+- без выравнивания, или с дубликатом первой папки с первой пустой ячейчи  - выравнивание либо влево, либо вправо

# обновление файла, не трогая уже имеющиеся, и помечая на удаление отсутвующие, новые в конец добавлять
# для этого нужно сперва чтение файла и путей из него
# словари по имени файлов со списками - путями? много памяти, зато можно помечать новые пить для таких же имен... а вот как помечать пути, которых теперь нет?

if __name__  == '__main__':
    main()