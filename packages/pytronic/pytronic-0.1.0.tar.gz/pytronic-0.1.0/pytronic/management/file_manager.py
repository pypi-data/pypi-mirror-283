import os
import json
import sys
from jinja2 import Environment, FileSystemLoader
from pytronic.utils import convert_to_snake_case


class FileManager:
    def __init__(self, base_dir='bots', template_dir='pytronic/templates'):
        self.base_dir = base_dir
        self.template_dir = template_dir

    def create_dir_bot(self, name: str, base_path=None):
        self._bot_name = name
        bot_name_snake_case = convert_to_snake_case(name)
        bot_dir = self._ensure_directory_exists(bot_name_snake_case)
        self._create_bot_file(bot_dir, bot_name_snake_case, name)
        self._create_task_json(bot_dir, base_path=base_path)
        self._create_task_schema(bot_dir)
        self._create_settings()

    def get_dir_bot(self):
        try:
            return f'{self.base_dir}/{convert_to_snake_case(self._bot_name)}'
        except AttributeError:
            return None

    def _create_task_schema(self, bot_dir):
        task_filename = os.path.join(bot_dir, 'task.py')
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('task_template.py.jinja')
        task_content = template.render()

        with open(task_filename, 'w') as f:
            f.write(task_content)

        return task_filename

    def _create_task_json(self, bot_dir, base_path=None):
        if base_path:
            bot_dir = os.path.join(base_path, bot_dir)
        task_filename = os.path.join(bot_dir, 'task.json')
        os.makedirs(bot_dir, exist_ok=True)
        if not os.path.exists(task_filename):
            with open(task_filename, 'w') as f:
                json.dump({}, f)

    def _ensure_directory_exists(self, sub_dir: str) -> str:
        base_path = os.path.join(self.base_dir)

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        sub_path = os.path.join(base_path, sub_dir)
        os.makedirs(sub_path, exist_ok=True)
        return sub_path

    def _create_bot_file(
        self, bot_dir: str, bot_name_snake_case: str, bot_classname: str
    ) -> str:
        bot_filename = os.path.join(bot_dir, f'{bot_name_snake_case}.py')
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('bot_template.py.jinja')
        bot_content = template.render(bot_classname=bot_classname)

        with open(bot_filename, 'w') as file:
            file.write(bot_content)

        return bot_filename

    def validate_bots_directory(self):
        current_directory = os.getcwd()
        bots_directory = os.path.join(current_directory, self.base_dir)

        if not os.path.exists(bots_directory):
            raise Exception(
                'The "bots" directory does not exist. Please run "pytronic init" first.'
            )

        sys.path.insert(0, bots_directory)

    def get_bot_module_path(self, bot_name_snake_case: str) -> str:
        return os.path.join(
            self.base_dir, bot_name_snake_case, f'{bot_name_snake_case}.py'
        )

    def check_bot_exists(self, bot_module_path: str, bot_name: str):
        if not os.path.exists(bot_module_path):
            raise Exception(
                f'Bot {bot_name} not found at the expected path: {bot_module_path}'
            )

    def load_default_task_file(self, bot_name_snake_case: str):
        task_file = os.path.join(
            self.base_dir, bot_name_snake_case, 'task.json'
        )

        if not os.path.exists(task_file):
            raise Exception(
                f'No task provided and the default file "{task_file}" was not found.'
            )

        with open(task_file, 'r') as f:
            return json.load(f)

    def _create_settings(self):
        settings_filename = os.path.join(self.base_dir, 'settings.py')
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('settings.py.jinja')
        settings_content = template.render(
            screenshots_path='images/screenshots',
            images_path='images',
            ocr_language='eng',
            screen_width=1920,
            screen_height=1080,
            pytesseract_path='/usr/bin/tesseract',
        )

        with open(settings_filename, 'w') as file:
            file.write(settings_content)

        return settings_filename
