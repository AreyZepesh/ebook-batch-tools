import csv
import json
# import re
from pathlib import Path
from datetime import datetime as dt

         
class BookFile():
    columns = [ 
    ("is_recommended","⭐"), #H
    ("author_folder","Автор(ы)/Межавторский цикл"),
    ("filename","Название файла"),
    ("is_read","Прочитано"), #H
    ("is_reading","В процессе"), #H
    ("is_dropped","Брошено"), #H
    ("has_paper_copy","Есть бумажная"), #H
    ("tags","Тэги"),
    ("fantlab_url","URL на фантлабе"),
    # ("handle_tags", "Мои Тэги"), #H
    # ("genres", "Жанры"),
    # ("description", "Описание")
    ("paths","Пути"),
    ("old_paths","Старые пути"),
    ("status","Статус"), # "new" / "ok" / "moved" / "missing"
        ]

    @classmethod
    def from_dict(cls, data: dict):
        book = cls.__new__(cls)
        for attr_name, attr_desc in cls.columns:
            value = data.get(attr_desc, 
                             data.get(attr_name, ""),
                             )
            setattr(book, attr_name, 
                    cls._value_from_table(attr_name, value),
                    )
        return book
    
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
    
    @classmethod
    def _value_from_table(cls, attr_name: str, value: str):
        if attr_name in ("tags", "paths"):
            if not value:
                return []
            try:
                return json.loads(value)
            except:
            # except json.JSONDecodeError as e:
                print("Не получилось декодировать JSON строку, возвращаю как есть")
                print(value)
                return value

        # if attr_name in ("is_recommended", "is_read", "is_reading", "is_dropped", "has_paper_copy"):
        # возможно так будет безопаснее, но с другой стороны - кто юзает тру/фолс в чистом виде?
        if value.upper() == "True".upper():
            return True
        if value.upper() == "False".upper():
            return False

        return value

    def get_table_row(self) -> list:
        return [self._value_for_table(attr_name) for attr_name, _ in self.columns]
    
    @classmethod
    def get_table_header(cls) -> tuple:
        return tuple([header for _, header in cls.columns])

def save_to_csv(csv_path, data: list):
    with open(csv_path,"w", encoding= "utf-8-sig") as file:
        csv_out = csv.writer(file, delimiter= ";", lineterminator= "\n")
        csv_out.writerow(BookFile.get_table_header())
        for item in data:
            csv_out.writerow( 
                item.get_table_row()
                ) 

def load_from_csv(csv_path):
    with open(csv_path, "r", encoding= "utf-8-sig") as file:
        return [BookFile.from_dict(x) for x in csv.DictReader(file, delimiter= ";")]


def main():
    filepath = f"./csv/{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    input_dir = Path("D:/Книги/По новому (выборка)")
    accept_file_ext = [".fb2",".epub",".pdf",".zip"]

    library = {}

    for file_path in Path(input_dir).glob("**/*"):
        if file_path.suffix in accept_file_ext:
            filename = file_path.stem
            rel_path = file_path.parent.relative_to(input_dir)
            if filename in library:
                library[filename].update_from_path(rel_path)
            else:
                library[filename] = BookFile( filename, rel_path )

    save_to_csv(filepath, library.values())

    old_lib = load_from_csv(filepath)
    print(old_lib[0].__dict__)
    print(
        type(old_lib[0].tags)
          )


if __name__ == '__main__':
    main()