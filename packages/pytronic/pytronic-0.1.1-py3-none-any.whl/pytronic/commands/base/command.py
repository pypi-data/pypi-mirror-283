import typer


class Command:
    @classmethod
    def register(cls, app: typer.Typer):
        command_instance = cls(app)
        command_name = cls.__name__.replace('Command', '').lower()
        app.command(name=command_name)(command_instance.execute)

    def __init__(self, app: typer.Typer):
        self.app = app

    def execute(self):
        raise NotImplementedError(
            'Subclasses must implement the execute method.'
        )
