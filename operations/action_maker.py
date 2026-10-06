from core.config import Action
from operations.replace_in_name import rename_file
from operations.zip_rename_root import rename_single_root_to_archive_name
from operations.zip_rename_name_and_root import rename_and_sync_root
from operations.zip_extract import zip_extract
from operations.pack_to_zip import pack_to_zip

def make_replace_in_name(
        accept_ext: tuple|list = (".fb2", ".epub", ".pdf", ".zip",),
        find_what: tuple|list = (".fb2",),
        replace_with: str = "",
        **kwargs):
    return Action(
        func = rename_file,
        accept_ext = accept_ext,
        kwargs = dict(
            find_what = find_what,
            replace_with = replace_with )
            )

def make_zip_rename_root(**kwargs):
    return Action(
        func = rename_single_root_to_archive_name,
        accept_ext = (".zip",),
            )

def make_zip_rename_name_and_root(
        find_what: tuple|list = (".fb2",),
        replace_with: str = "",
        **kwargs):
    return Action(
        func = rename_and_sync_root,
        accept_ext = (".zip",),
        kwargs = dict(
            find_what = find_what,
            replace_with = replace_with )
            )

def make_zip_extract(
        zip_filename_encoding: str | None = None, 
        verify_extracted=True, 
        **kwargs):
    """zip_filename_encoding: может быть cp437, cp866, cp1251, utf-8 и другими кодировками\n
    verify_extracted: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве"""
    return Action(
        func = zip_extract,
        accept_ext = (".zip",),
        kwargs = dict(zip_filename_encoding = zip_filename_encoding,
                      verify_extracted = verify_extracted )
            )

def make_pack_to_zip(accept_ext: tuple|list = (".fb2",),
                            verify_packed: bool = False,
                            save_suffix_in_name: bool = False, 
                            **kwargs):
    """verify_packed: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве\n 
    save_suffix_in_name: Если нужно сохранить расширение архивированного файла в имени архива"""
    return Action(
        func = pack_to_zip,
        accept_ext = accept_ext,
        kwargs = dict(verify_packed = verify_packed,
                      save_suffix_in_name = save_suffix_in_name )
            )