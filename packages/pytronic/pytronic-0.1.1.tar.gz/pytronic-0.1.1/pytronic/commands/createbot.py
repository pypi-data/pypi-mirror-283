import typer
from pytronic.commands.base.command import Command
from pytronic.management import FileManager


class CreateBot(Command):
    def execute(self, name: str):
        """Creates a new bot with the specified name."""
        FileManager().create_dir_bot(name)
        typer.echo(f'Created in /bots a new bot: {name}')
