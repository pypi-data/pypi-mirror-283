import os, json, importlib, inspect
from pydantic import BaseModel
from pytronic.utils import convert_to_snake_case
from pytronic.management.file_manager import FileManager
from pytronic.bot import Bot


class BotLoader:
    def __init__(self, bot_name: str, task: str = None, file_manager=None):
        self.file_manager = file_manager or FileManager()
        self._bot_name = bot_name
        self._task = task

    def get(self) -> Bot:
        bot_name_snake_case = convert_to_snake_case(self._bot_name)
        self.file_manager.validate_bots_directory()

        bot_module_path = self.file_manager.get_bot_module_path(
            bot_name_snake_case
        )

        self.file_manager.check_bot_exists(bot_module_path, self._bot_name)
        bot_dict = self._load_bots(bot_name_snake_case)
        task_schema = self._load_task_schema(bot_name_snake_case)
        return self._get_bot_instance(
            bot_dict, bot_name_snake_case, task_schema
        )

    def _load_task_schema(self, bot_name_snake_case: str):
        task_module_name = (
            f'{self.file_manager.base_dir}.{bot_name_snake_case}.task'
        )
        task_module = importlib.import_module(task_module_name)
        for name, obj in inspect.getmembers(task_module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseModel)
                and obj is not BaseModel
            ):
                return obj
        raise Exception(f'Task schema not found for bot {bot_name_snake_case}')

    def _load_bots(self, bot_name_snake_case: str):
        module_name = f'{bot_name_snake_case}.{bot_name_snake_case}'
        module = importlib.import_module(module_name)
        bots = self._get_bot_classes(module)
        return {bot.__name__: bot for bot in bots}

    @staticmethod
    def _get_bot_classes(module):
        return [
            obj
            for _, obj in inspect.getmembers(module)
            if inspect.isclass(obj) and issubclass(obj, Bot) and obj is not Bot
        ]

    def _get_bot_instance(
        self, bot_dict: dict, bot_name_snake_case: str, task_schema: BaseModel
    ):
        if self._bot_name in bot_dict:
            task_data = self._load_task_data(bot_name_snake_case)
            bot_strategy = bot_dict[self._bot_name]
            return bot_strategy(task=task_schema(**task_data))
        raise Exception(f'Bot {self._bot_name} not found.')

    def _load_task_data(self, bot_name_snake_case: str) -> dict:
        if self._task:
            return self._load_task_from_string_or_file(self._task)
        return self.file_manager.load_default_task_file(bot_name_snake_case)

    @staticmethod
    def _load_task_from_string_or_file(task: str) -> dict:
        if os.path.isfile(task):
            with open(task, 'r') as f:
                return json.load(f)
        try:
            task_string = task.replace("'", '"')
            return json.loads(task_string)
        except json.JSONDecodeError:
            raise Exception(
                'The --task argument is not a valid JSON or an existing file path.'
            )
