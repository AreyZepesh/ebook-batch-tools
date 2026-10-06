import traceback
from core.config import Config
from core.path_mapping import PathMapping
from core.action_result import ActionResult

from core.logger import setup_logging, q
logger = setup_logging()

def walk_and_edit(config: Config) -> None:
    if config.action is None:
        logger.error("config.action is None")
        raise ValueError("config.action обязателен")
    
    logger.debug("Конфигурация: %s", config.__dict__ )
    accept_ext = {ext.lower() for ext in config.action.accept_ext}
    logger.debug("Разрешенные для обработки расширения: %s", accept_ext )
    file_list: list[PathMapping] = list(config.input_dir.glob("**/*"))
    logger.debug("Объктов (файл/папка) найдено: %i", len(file_list) )

    for file_path in file_list:
        logger.debug("Обработка: %s", q(file_path) )
        if not file_path.is_file():
            logger.debug("%s не является файлом", q(file_path) )
            continue
        if file_path.suffix.lower() not in accept_ext:
            logger.debug("%s не имеет разрешенного расширения", q(file_path) )
            continue
        if config.output_dir:
            logger.debug("Замена %s в целевом пути на %s", q(config.input_dir), q(config.output_dir) )
            file_path.remap_dst_path(config.input_dir, config.output_dir)
        logger.debug("Нужна копия с сохранением оригинала: %s", config.need_copy )
        file_path.need_copy_to_dst = config.need_copy

        try:
            logger.debug("Попытка обработки в: %s ", q(config.action.func.__name__))
            action_result: ActionResult = config.action(file_path)
        except Exception:
            logger.error("%s: %s", q(file_path), traceback.format_exc() )
            continue
        
        if not isinstance(action_result, ActionResult):
            txt_error = f"{q(file_path)}: Функция {config.action.func.__name__} вернула неожиданный результат или None: {action_result}"
            logger.error(txt_error)
            raise TypeError(txt_error)
        
        logger.debug("action_result: change_confirmed = %s, safe_to_remove_source = %s", action_result.change_confirmed, action_result.safe_to_remove_source )

        if action_result.can_remove_source():
            file_path.remove()
            logger.info("Удален исходный файл: %s", q(file_path))
        
        print() # декаратив для терминала