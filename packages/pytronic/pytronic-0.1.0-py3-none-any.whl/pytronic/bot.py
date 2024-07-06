from pydantic import BaseModel


class Bot:
    def __init__(self, task: BaseModel):
        self.task = task

    def run(self):
        raise NotImplementedError(
            'O método run deve ser implementado pela subclasse'
        )
