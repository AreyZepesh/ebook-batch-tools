from common import PathMapping, ActionResult, walk_and_edit

from replace_in_name import rename_file
from zip_rename_root import rename_single_root_to_archive_name
from zip_rename_name_and_root import rename_and_sync_root
from zip_extract import zip_extract
from pack_to_zip import pack_to_zip

def run(): ...

def main(): # zip_and_file_rename
    accept_file_ext_to_change = [".zip"]

def main(): # replace_in_name + rename_zip_and_root
    find_what_replaced = [".fb2", ".epub"]
    replace_with = ""

def main(): # zip_extract
    accept_file_ext_to_change = [".zip"]

    zip_filename_encoding = "cp866",
    # verify_extracted = False

def main(): # zip_pack_one_file
    accept_file_ext_to_change = [".fb2"]
    verify_packed = True,
    # save_suffix_in_name = True


class Config:
    # all
    input_dir = "D:\\Книги\\_update"
    output_dir = "D:\\Книги\\_update2"
    need_copy = True

    accept_file_ext_to_change = [".fb2", ".zip"]

    # rename_zip_and_root
    find_what_replaced = [".fb2", ".epub", ".pdf"] # [".zip"]
    replace_with = ""

    # zip_extract
    zip_filename_encoding = "cp866", # None
    # zip_filename_encoding: может быть cp437, cp866, cp1251, utf-8
    verify_extracted = True # True
    # verify_extracted: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве
    
    # zip_pack_one_file
    verify_packed = True, # Fasle
    # verify_packed: Если нужна дополнительная сверка извлеченного файла, с исходным в архиве 
    save_suffix_in_name = True # Fasle
    # save_suffix_in_name: Если нужно сохранить расширение архивированного файла в имени архива

walk_and_edit(
    # input_dir = input_dir, 
    # action_func = pack_to_zip, 
    # output_dir = output_dir,
    # need_copy = need_copy,
    # accept_file_ext_to_change = accept_file_ext_to_change,
    # func_kwargs = dict(),
    )

# NOTE: accept_file_ext_to_change только zip должен быть в: 
# rename_single_root_to_archive_name 
# zip_extract
