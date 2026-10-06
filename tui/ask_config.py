from core.config import Config

from operations.action_maker import (
    make_pack_to_zip, 
    make_replace_in_name, 
    make_zip_extract, 
    make_zip_rename_name_and_root, 
    make_zip_rename_root)

def print_welcome():
    print("Привет! Для получения справки по текущему вводу, введите -h.",
            "   Для выхода из программы нажмите CTRL+C",
            sep = "\n")

def get_input_dir():
    answer = input("Введите путь к папке c файлами для обработки: ")
    if answer.lower() == "-h":
        print("   Путь должен указывать на существующую директорию, ",
            "в случае если её не существует необходим повторный ввод. ",
            "Для работы в текущей директории введите '.'",
            "Текущая директория: папка, где лежит исполняемый файл этой программы.", 
            sep="\n   "
            )
        answer = get_input_dir()
    if not answer:
        return None
    return answer

def get_output_dir():
    answer = input("Введите путь к папке для сохранения результатов: ")
    if answer.lower() == "-h":
        print("   В данную папку будут сохранены результаты обратотки исходных файлов.",
            "Можно указывать не существующую конечную директорию, в таком случае она будет создана, если это возможно",
            "Данный путь можно не указывать, в таком случае файлы будут сохраняться рядом с исходными.",
            "Сохранение файлов вместо исходных возможно, смотрите следующий пункт настроек.",
            "Для работы в текущей директории введите '.'",
            "Текущая директория: папка, где лежит исполняемый файл этой программы.", 
            sep="\n   "
            )
        answer = get_output_dir()
    if not answer:
        return None
    return answer

def get_need_copy():
    answer = input("Нужно ли сохранить исходные файлы после изменений? (Y/n): ")
    if answer.lower() == "-h":
        print("   Не рекомендуется отключать данную опцию!", 
              "В случае отрицательного значения, исходные файлы будут:", 
              " - удалены, в случае если указана папка для сохранения результатов", 
              " - заменены, в случае если она не указана", 
              "Удаление необратимо! Удаленные файлы не попадут в корзину", 
            sep="\n   ")
        return get_need_copy()

    if answer.lower() == "n":
        if input("Вы точно уверены? Исходные файлы будут удалены или заменены (y/N):").lower() == "y":
            print("Исходные файлы будут удалены (Только обработанные файлы)")
            return False
        else: 
            print("Отмена, сохраняем исходные файлы")
    else:
        if answer and answer.lower() != "y":
            print("Не удалось интерпритировать ответ, установлено значение по умолчанию: ")
        print("Исходные файлы будут сохранены")

    return True

def get_():
    answer = input()
    if answer.lower() == "-h":
        print("   ", 
              "", 
            sep="\n   ")
        answer = get_()
    if not answer:
        return None
    return answer

def get_config():
    # import os
    # os.system("clear||cls")
    cfg = Config(input_dir=get_input_dir())
    cfg.output_dir = get_output_dir()
    cfg.need_copy = get_need_copy()

    act = ...
    return cfg

def main():
    print_welcome()
    end = False
    while not end:
        try:
            cfg = get_config()
        except KeyboardInterrupt:
            end = True
            continue
        except ValueError as ex:
            print(ex)
            continue
        print(cfg.__dict__)
        end = True


"""Что делаем при запуске? получаем вопросы о том что делать.
Для cli: предлогаем выбор: работать или справку. Если будет gui - там менюхами. Работа:
Спрашиваем:
    +1. ОТКУДА работать: input_dir
    2. КУДА работать? output_dir - можно пустое, тогда сохраняет рядом с исходником (или вместо)
    3. Нужно ли сохранять оригинал, Если нет - переспросить. Особенно если не указан output_dir
    4. Что будем делать? выбор из 5 вариантов
    5. Как это делать? Уточнение параметров, там где это возможность
Показываем выбранные параметры, спрашиваем - всё ли верно? 
При подтверждении - производим действие, выводим лог"""