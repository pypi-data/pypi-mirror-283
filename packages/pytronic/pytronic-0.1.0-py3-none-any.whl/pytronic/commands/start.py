import typer, os
from pytronic.commands.base.command import Command
from pytronic.management import FileManager


class Start(Command):
    def execute(self):
        """Initializes the project by creating the necessary folders and an example bot."""
        if not os.path.exists('bots'):
            os.makedirs('bots')
            typer.echo("path 'bots/' created.")

        FileManager().create_dir_bot('Example')
