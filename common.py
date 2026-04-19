import shutil
from pathlib import Path
from datetime import datetime as dt

# TODO возможно уйти от os к pathlib?
import os
import zipfile
import traceback
import tempfile

class PathMapping(Path):
    def __init__(self, *args):
        super().__init__(*args)
        self.src_path = Path(self)
        self.ignore_exists_dst = False
        self._dst_path = Path(self)
        self.need_copy_to_dst = True

    def remap_dst_path(self, input_dir, output_dir):
        """replace in dst_path"""
        relative = self.relative_to(input_dir)
        self._dst_path = Path(output_dir, relative) 

    def replace_in_dst_stem(self, find_what: str, replace_with: str):
        """replace in dst_path.stem"""
        self._dst_path = self._dst_path.with_stem(
            self._dst_path.stem.replace(find_what, replace_with)
            )

    @property
    def dst_path(self):
        """lazy resolve\n
        Resolve and persist final destination path."""
        self._dst_path = self.get_destination_path(self.ignore_exists_dst)
        return self._dst_path
    
    @dst_path.setter
    def dst_path(self, path):
        self._dst_path = Path(path)
    
    @dst_path.deleter
    def dst_path(self):
        self._dst_path = Path(self)

    def _is_src_same_dst(self):
        return self.src_path.resolve(strict=False) == self._dst_path.resolve(strict=False)
    
    def should_transfer(self):
        return not self._is_src_same_dst()

    def should_delete_source(self):
        # print(f"{self.src_path.resolve(strict=False)=}\n{self._dst_path.resolve(strict=False)=}")
        # print(f"{self._is_src_same_dst()=}")
        # print(f"{self.need_copy_to_dst=}")
        # print(f"{self.src_path.exists()=}")
        if self._is_src_same_dst():
            return False
        if self.need_copy_to_dst:
            return False
        return self.src_path.exists()


    def get_destination_path(self, ignore_exists = False):
        dst_path = self._dst_path

        if ignore_exists:
            return dst_path
        
        if self._is_src_same_dst() and not self.need_copy_to_dst:
            return dst_path

        if dst_path.exists():
            # print(f"Файл уже сушествует: {dst_path}")
            dst_path = dst_path.with_stem(dst_path.stem + "_copy")
        if dst_path.exists():
            # print(f"Файл уже сушествует: {dst_path}")
            dst_path = dst_path.with_stem(dst_path.stem + f"_{dt.now().strftime("%Y%m%d%H%M%S")}")

        return dst_path
    
    def remove(self):
        os.remove(self.src_path)

    def copy(self, target: Path):
        # if not target.exists() or not os.path.samefile(self, target):
        #     shutil.copy(self, target)
        # else:
        #     print(f"Тот же файл: {target}")
        #     raise shutil.SameFileError
        shutil.copy(self, target)

    def transfer(self) -> Path:
        """Перемещение или копирование в dst_path \n
        Возращает конечный путь"""
        dst_path: Path = self.dst_path

        # создаем папку, если её нет
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        # копируем, если надо - иначе переносим
        # if self.need_copy_to_dst:
        #     self.copy(dst_path)
        # else:
        #     self.replace(dst_path)
        # переделываю под логику удаление в одном месте

        self.copy(dst_path)
        return dst_path




def walk_and_edit(
        input_dir: str | Path, 
        action_func, 
        output_dir: str | Path | None = None, 
        need_copy: bool = True,
        accept_file_ext_to_change: list = [".zip"],
        func_kwargs: dict = None,
            ) -> None:
    
    for file_path in PathMapping(input_dir).glob("**/*"):
        if not file_path.is_file():
            continue
        if not file_path.suffix in accept_file_ext_to_change:
            continue
        if output_dir:
            file_path.remap_dst_path(input_dir,output_dir)

        file_path.need_copy_to_dst = need_copy

        change_confirmed = action_func(file_path = file_path,
                                **func_kwargs or {})
        
        if change_confirmed and not need_copy:
            file_path.remove()
            print(f"!   Удален исходный файл: {file_path}")
        


