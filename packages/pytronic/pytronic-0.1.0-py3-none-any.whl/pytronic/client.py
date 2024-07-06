import typer
from pytronic.commands.start import Start
from pytronic.commands.createbot import CreateBot
from pytronic.commands.run import Run

app = typer.Typer()

Start.register(app)
CreateBot.register(app)
Run.register(app)

if __name__ == '__main__':
    app()
