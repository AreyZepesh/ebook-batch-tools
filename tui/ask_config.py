from core.config import Config, Action

from operations.action_maker import (
    make_pack_to_zip, 
    make_replace_in_name, 
    make_zip_extract, 
    make_zip_rename_name_and_root, 
    make_zip_rename_root)

# import os
# os.system("clear||cls")
OPERATIONS = {"1": dict(func = make_replace_in_name, 
                            txt = "Замена в имени файла;" , 
                            help = ["Заменяет S1 на S2 в имени файла, не затрагивая путь или расширение",
                                    "Пример: есть N файлов: 'sample_N.fb2.zip'",
                                    "Нужно заменить '.fb2' (S1) в имени файлов на '' или '_ebook' (S2)",
                                    "Операция произведет замену во всех файлах, подходящих под параметры",
                                    "На выходе файлы будут называться: 'sample_N.zip' или 'sample_N_ebook.zip' соответвенно"
                                    ],
                            ),
                  "2": dict(func = make_pack_to_zip, 
                            txt = "Упаковать файлы в индивидуальные zip архивы;" , 
                            help = ["Упаковывает каждый в файл в отдельный архив.",
                                    "Т.е. сколько было исходных файлов, столько же архивов будет на выходе",
                                    ],
                            ),
                  "3": dict(func = make_zip_rename_root, 
                            txt = "Переименовать файл/папку в корне архива на имя данного архива (только .zip);" , 
                            help = ["Данная функция работает только с архивами в корне которого находится только один файл или папка.",
                                    "Операция синхронизирует имя корневого элемента архива с именем самого архива",
                                    "Пример: есть N архивов: 'sample_N.zip', содержажих 'dir/ebook.fb2' или 'super.fb2'",
                                    "Итог: в каждом таком архиве будет содержаться папка 'sample_N/ebook.fb2' или 'sample_N.fb2'",
                                    ],
                            ),
                  "4": dict(func = make_zip_rename_name_and_root, 
                            txt = "Операции 1 и 3 последовательно. Замена в имени архива, и переименовать файл/папку в корне архива (только .zip);" , 
                            help = ["Данная функция работает только с архивами в корне которого находится только один файл или папка.",
                                    "Заменяет S1 на S2 в имени файла, не затрагивая путь или расширение, а так же меняет имя корневого элемента архива",
                                    "Пример: есть N архивов: 'sample_N.fb2.zip', содержажих 'dir/ebook.fb2' или 'super.fb2'",
                                    "Нужно заменить '.fb2' (S1) в имени архивов на '' или '_ebook' (S2)",
                                    "Итог: получим архивы 'sample_N.zip' содержащие 'sample_N/ebook.fb2' или 'sample_N.fb2'",
                                    "или архивы 'sample_N_ebook.zip' содержащие 'sample_N_ebook/ebook.fb2' или 'sample_N_ebook.fb2' соответвенно",
                                    ],
                            ),
                  "5": dict(func = make_zip_extract, 
                            txt = "Распаковать архивы (только .zip);" , 
                            help = ["Распаковывает каждый архив в соответвии с указанными параметрами",
                                    ],
                            ),}

def print_welcome():
    print("Привет! Для получения справки по текущему вводу, введите -h.",
            "   Для выхода из программы нажмите CTRL+C",
            sep = "\n")

def get_input_dir():
    answer = input("Введите путь к папке c файлами для обработки: ").strip()
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
    answer = input("Введите путь к папке для сохранения результатов: ").strip()
    if answer.lower() == "-h":
        print("   В данную папку будут сохранены результаты обратотки исходных файлов.",
            "Данный путь можно не указывать, в таком случае файлы будут сохраняться рядом с исходными.",
            "Можно указывать не существующую конечную директорию, в таком случае она будет создана, если это возможно",
            "Сохранение файлов происходит с сохранением дерева, относительно начальной папки:",
            "т.е если файл был в 'input/dir1/dir2/file' то сохранение будет в 'output/dir1/dir2/file' ",
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
    answer = input("Нужно ли сохранить исходные файлы после изменений? (Y/n): ").strip()
    if answer.lower() == "-h":
        print("   Не рекомендуется отключать данную опцию!", 
              "В случае отрицательного значения, исходные файлы будут:", 
              " - удалены, в случае если указана папка для сохранения результатов", 
              " - заменены, в случае если она не указана", 
              "Удаление необратимо! Удаленные файлы не попадут в корзину", 
            sep="\n   ")
        return get_need_copy()

    if answer.lower() == "n":
        if input("Вы точно уверены? Исходные файлы будут удалены или заменены (y/N):").lower().strip() == "y":
            print("Исходные файлы будут удалены (Только обработанные файлы)")
            return False
        else: 
            print("Отмена, сохраняем исходные файлы")
    else:
        if answer and answer.lower() != "y":
            print("Не удалось интерпритировать ответ, установлено значение по умолчанию: ")
        print("Исходные файлы будут сохранены")

    return True

def get_operation():
    help = "Для более подробной информации по операциям, введите -h N, где N номер операции"
    txt = "Доступные операции с файлами:\n"
    for k, v in OPERATIONS.items():
            txt += f" {k}. {v.get("txt")} \n"
    txt += help

    print(txt)
    answer = None
    while not answer in OPERATIONS.keys():
        answer = input("Ожидается ввод: ").strip()
        if not answer:
            continue
        if answer in OPERATIONS.keys():
            break
        
        answer = answer.lower()
        if answer == "-h":
            print("   ",help)
            continue
        if len(answer) >= 4:
            if answer[:2] == "-h" and answer[-1] in OPERATIONS.keys():
                for s in OPERATIONS.get(answer[-1]).get("help"):
                    print("   ", s)

    return OPERATIONS.get(answer).get("func")

def get_():
    answer = input().strip()
    if answer.lower() == "-h":
        print("   ", 
              "", 
            sep="\n   ")
        answer = get_()
    if not answer:
        return None
    return answer

def get_config() -> Config:

    cfg = Config(input_dir=get_input_dir())
    cfg.output_dir = get_output_dir()
    cfg.need_copy = get_need_copy()
    return cfg

def get_actioin() -> Action:
    act = get_operation()
    if act is None:
        return None
    ...
    return act()

def main():
    print_welcome()
    end = False
    while not end:
        try:
            # cfg = get_config()
            # cfg.action = get_actioin()
            action = get_actioin()
        except KeyboardInterrupt:
            end = True
            continue
        except ValueError as ex:
            print(ex)
            continue
        print(action.__dict__)
        end = True


"""Что делаем при запуске? получаем вопросы о том что делать.
Для cli: предлогаем выбор: работать или справку. Если будет gui - там менюхами. Работа:
Спрашиваем:
    +1. ОТКУДА работать: input_dir
    +2. КУДА работать? output_dir - можно пустое, тогда сохраняет рядом с исходником (или вместо)
    +3. Нужно ли сохранять оригинал, Если нет - переспросить. Особенно если не указан output_dir
    4. Что будем делать? выбор из 5 вариантов
    5. Как это делать? Уточнение параметров, там где это возможность
Показываем выбранные параметры, спрашиваем - всё ли верно? 
При подтверждении - производим действие, выводим лог"""