import csv
import json
# import re
from pathlib import Path
from datetime import datetime as dt

         
class BookFile():
    columns = [ 
    ("is_recommended","⭐"),
    ("author_folder","Автор(ы)/Межавторский цикл"),
    ("filename","Название файла"),
    ("is_read","Прочитано"),
    ("is_reading","В процессе"),
    ("is_dropped","Брошено"),
    ("has_paper_copy","Есть бумажная"),
    ("tags","Тэги"),
    ("paths","Пути"),
    ("fantlab_url","URL на фантлабе"),
    # ("", ""),
    # ("genres", "Жанры"),
    # ("description", "Описание")
        ]
    
    def __init__(self, filename, path):
        # type(self).all_files[]
        self.is_recommended = False
        self.author_folder = ""
        self.filename = filename
        self.is_read = False
        self.is_reading = False
        self.is_dropped = False
        self.has_paper_copy = False
        self.tags = []
        self.paths = []
        self.fantlab_url = ""
        self.update_from_path(path)

    def update_from_path(self, new_path):
        path = Path(new_path)
        self.add_path(str(path))
        parts = path.parts
        self.update_author_folder (parts[-1])
        self.add_tag(parts[0])

    def update_author_folder (self, new_author_folder ):
        if self.author_folder == "":
            self.author_folder = new_author_folder 
        elif self.author_folder == new_author_folder :
            pass
        elif self.author_folder  in new_author_folder  or new_author_folder  in self.author_folder :
            self.author_folder = self.author_folder  if len(self.author_folder ) > len(new_author_folder ) else new_author_folder 
        elif self.author_folder  != new_author_folder :
            self.author_folder  += f"\n{new_author_folder }"

            
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def add_path(self, path: str):
        if path not in self.paths:
            self.paths.append(path)

    def _value_for_table(self, attr_name):
        value = getattr(self, attr_name, "")
        if attr_name == "fantlab_url" and not value:
            title = self.filename.split(". ")[-1]
            # title = re.sub(r"\d()", "", title)
            title = title.strip()
            return f"https://fantlab.ru/search/?searchstr={title}"
        if isinstance(value, list):
            return json.dumps(value, ensure_ascii=False)

        return value
    
    def get_table_row(self) -> list:
        return [self._value_for_table(attr_name) for attr_name, _ in self.columns]
    
    @classmethod
    def get_table_header(cls) -> tuple:
        return tuple([header for _, header in cls.columns])


def main():
    filepath = f"./csv/{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    input_dir = Path("D:/Книги/По новому (выборка)")
    accept_file_ext = [".fb2",".epub",".pdf",".zip"]

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


    with open(filepath,"a", encoding= "utf-8-sig") as file:
        csv_out = csv.writer(file, delimiter= ";", lineterminator= "\n")
        csv_out.writerow(BookFile.get_table_header())
        for item in library.values():
            csv_out.writerow( 
                item.get_list_from_table_row()
                ) 
        


if __name__ == '__main__':
    main()