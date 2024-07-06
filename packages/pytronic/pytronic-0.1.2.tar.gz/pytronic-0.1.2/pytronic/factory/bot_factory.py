from pytronic.management import BotLoader
from pytronic.bot import Bot
from pytronic.management import FileManager


class BotFactory:
    def __init__(self, bot_name: str, task: str | dict = None):
        self.bot_name = bot_name
        self.task = task if not isinstance(task, dict) else str(task)

    def create(self, dir_exists=False) -> Bot:
        if not dir_exists:
            FileManager().create_dir_bot(self.bot_name)
        return BotLoader(self.bot_name, self.task).get()
