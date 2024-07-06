import typer
from pytronic.commands.base.command import Command
from pytronic.factory.bot_factory import BotFactory


class Run(Command):
    def execute(
        self,
        bot_name: str,
        task: str = typer.Option(None, help='Task for the bot to execute'),
    ):
        """Executes a bot with the specified task."""
        bot = BotFactory(bot_name, task).create(dir_exists=True)
        bot.run()
