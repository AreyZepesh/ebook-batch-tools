import shutil
from pathlib import Path
from datetime import datetime as dt

# TODO возможно уйти от os к pathlib?
import os
import zipfile
import traceback
import tempfile
from dataclasses import dataclass, field

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
    
    def set_dst_stem(self, new_stem):
        self._dst_path = self._dst_path.with_stem(new_stem)
        return self._dst_path
        
    def set_dst_suffix(self, new_suffix):
        self._dst_path = self._dst_path.with_suffix(new_suffix)
        return self._dst_path
    
    def get_dst_stem(self) -> str:
        return self._dst_path.stem
    
    def dst_stem_changed(self) -> str:
        return self.src_path.stem != self._dst_path.stem

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
    
    def src_is_same(self, target):
        return self.src_path.resolve(strict=False) == Path(target).resolve(strict=False)
    
    def should_transfer(self):
        return not self._is_src_same_dst()

    def should_delete_source(self):
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
            dst_path = dst_path.with_stem(dst_path.stem + "_copy")
        if dst_path.exists():
            dst_path = dst_path.with_stem(dst_path.stem + f"_{dt.now().strftime("%Y%m%d%H%M%S")}")

        return dst_path
    
    def remove(self):
        os.remove(self.src_path)

    def copy(self, target: Path):
        shutil.copy(self, target)

    def transfer(self) -> Path:
        """Перемещение или копирование в dst_path \n
        Возращает конечный путь"""
        dst_path: Path = self.dst_path
        # создаем папку, если её нет
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        self.copy(dst_path)
        return dst_path

@dataclass
class ActionResult():
    change_confirmed: bool = field(default=False)
    safe_to_remove_source: bool = field(default=False)

    def can_remove_source(self):
        return self.change_confirmed and self.safe_to_remove_source

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

        # if accept_file_ext_to_change and len(accept_file_ext_to_change) > 0 : 
        # NOTE если нужно проходить все файлы, если не указано расширение
        if not file_path.suffix in accept_file_ext_to_change:
            continue
        if output_dir:
            file_path.remap_dst_path(input_dir,output_dir)

        file_path.need_copy_to_dst = need_copy

        action_result: ActionResult = action_func(file_path = file_path,
                                **func_kwargs or {})
        
        if not isinstance(action_result, ActionResult):
            raise Exception(f"Функция {action_func.__name__} вернула None")
        
        if action_result.can_remove_source(): # and not need_copy:
            file_path.remove()
            print(f"!   Удален исходный файл: {file_path}")
        

