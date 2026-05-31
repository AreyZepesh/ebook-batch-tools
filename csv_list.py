from pathlib import Path
import csv
import json
from datetime import datetime as dt
from typing import Any
         
class BookFile():
    #TODO привязать к реализации данные колонки
    columns = [ 
    ("is_recommended", "⭐"),
    ("filefolder", "Автор(ы)/Межавторский цикл"),
    ("filename", "Название файла"),
    ("is_readed", "Прочитано"),
    ("is_in_reading", "В процессе"),
    ("is_in_droped", "Брошено"),
    ("is_in_paper", "Есть бумажная"),
    ("tags", "tag"),
    ("paths", "pathes"),
    ("url", "URL на фантлабе"),
        ]
    
    def __init__(self, filename, path):
        # type(self).all_files[]
        self.is_recommended = False #0
        self.filefolder = "" #1
        self.filename = filename #2
        self.is_readed = False #3
        self.is_in_reading = False #4
        self.is_in_droped = False #5
        self.is_in_paper = False #6
        self.tags = [] #7
        self.paths = [] #8
        self.url = "" #9
        # self.filename = Attr(value=filename, header='Название файла', priority=2)
        # self.path = Attr(value=path, header='Пути', priority=8)
        # self. = Attr(value=, header='', priority=)
        
        self.update_from_path(path)


    def update_from_path(self, new_path):
        path = Path(new_path)
        self.add_path(str(path))
        parts = path.parts
        self.update_filefolder(parts[-1])
        self.add_tag(parts[0])

    def update_filefolder(self, new_filefolder):
        if self.filefolder == "":
            self.filefolder = new_filefolder
        elif self.filefolder == new_filefolder:
            pass
        elif self.filefolder in new_filefolder or new_filefolder in self.filefolder:
            self.filefolder = self.filefolder if len(self.filefolder) > len(new_filefolder) else new_filefolder
        elif self.filefolder != new_filefolder:
            self.filefolder += f"\n{new_filefolder}"

            
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def add_path(self, path: str):
        if path not in self.paths:
            self.paths.append(path)

    def get_list_from_table_row(self):
        #TODO уйти от этого чтения и подключить серилизацию json
        # json.dumps(self.paths/tags, ensure_ascii=False)
        # return self.__dict__.items()
        return list(self.__dict__.values())
    
    @classmethod
    def _get_table_header(cls) -> tuple:
        return tuple([
            '⭐',#0.encode().decode('cp1251'), 
            'Автор(ы)/Межавторский цикл', #1 последний part пути
            'Название файла', #2 filename
            'Прочитано', #3 bool
            'В процессе', #4 bool
            'Брошено', #5 bool
            'Есть бумажная', #6 bool
            'tag', #7 первая после рута часть пути
            'pathes', #8 список/сет путей
            'URL на фантлабе', #9 https://fantlab.ru/search/?searchstr= + filemane/автор
            # '',
            # 'Жанры', # экспорты из старых только, либо делать парсящую функцию,
            # 'Описание',
                ])


def main():
    filepath = f"./csv/{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    input_dir = Path("D:/Книги/По новому (выборка)")
    accept_file_ext = [".fb2", ".epub", ".pdf", ".zip"]

    library = {}

    # for dirpath, _, filenames in Path(input_dir).walk():
    #     for filename in filenames:
    #         if Path(filename).suffix in accept_file_ext:
    #             items.append(
    #                 BookFile( filename, dirpath.relative_to(input_dir) )
    #                 )

    for file_path in Path(input_dir).glob("**/*"):
        if file_path.suffix in accept_file_ext:
            filename = file_path.stem
            rel_path = file_path.parent.relative_to(input_dir)
            if filename in library:
                library[filename].update_from_path(rel_path)
            else:
                library[filename] = BookFile( filename, rel_path )


    with open(filepath, "a", encoding="utf-8-sig") as file:
        csv_out = csv.writer(file, delimiter=";", lineterminator="\n")
        csv_out.writerow(BookFile._get_table_header())
        for item in library.values():
            csv_out.writerow( 
                item.get_list_from_table_row()
                ) 
        


if __name__  == '__main__':
    main()