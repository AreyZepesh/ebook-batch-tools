import shutil
from pathlib import Path
from datetime import datetime as dt

from core.safe_path import get_safe_name

class PathMapping(Path):
    def __init__(self, *args):
        super().__init__(*args)
        self.src_path = Path(self)
        self.ignore_exists_dst = False
        self._dst_path = Path(self)
        self.need_copy_to_dst = True
        self._dst_resolved = False

    def remap_dst_path(self, input_dir, output_dir):
        """replace in dst_path"""
        relative = self.relative_to(input_dir)
        self._dst_path = Path(output_dir, relative) 
        self._dst_resolved = False

    def replace_in_dst_stem(self, find_what: str, replace_with: str):
        """replace in dst_path.stem"""
        new_stem = self._dst_path.stem.replace(find_what, replace_with)
        self._dst_path = self._dst_path.with_stem(
            get_safe_name(new_stem, is_stem=True)
                )
        self._dst_resolved = False
    
    def set_dst_stem(self, new_stem):
        self._dst_path = self._dst_path.with_stem(get_safe_name(new_stem, is_stem=True))
        self._dst_resolved = False
        return self._dst_path
        
    def set_dst_suffix(self, new_suffix):
        self._dst_path = self._dst_path.with_suffix(new_suffix)
        self._dst_resolved = False
        return self._dst_path
    
    def get_dst_stem(self) -> str:
        return self._dst_path.stem
    
    def dst_stem_changed(self) -> bool:
        return self.src_path.stem != self._dst_path.stem

    @property
    def dst_path(self):
        """lazy resolve\n
        Resolve and persist final destination path.\n
        Резолвит один раз и кэширует результат."""
        if not self._dst_resolved:
            self._dst_path = self.get_destination_path(self.ignore_exists_dst)
            self._dst_resolved = True
        return self._dst_path
    
    @dst_path.setter
    def dst_path(self, path):
        self._dst_path = Path(path)
        self._dst_resolved = True
    
    @dst_path.deleter
    def dst_path(self):
        self._dst_path = Path(self)
        self._dst_resolved = False

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
        # os.remove(self.src_path)
        self.src_path.unlink(missing_ok=True)

    def copy(self, target: Path):
        shutil.copy(self, target)

    def transfer(self) -> Path:
        """Перемещение или копирование в dst_path \n
        Возвращает конечный путь"""
        dst_path = self.dst_path
        # создаем папку, если её нет
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        self.copy(dst_path)
        return dst_path
