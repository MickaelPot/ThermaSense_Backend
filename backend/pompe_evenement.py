from django.db import models
import asyncio

class Evenement(models.Model):
    name = models.CharField(max_length=100)

class FunctionEvent:
    def __init__(self, function_name, *args, **kwargs):
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs

    async def execute(self):
        # Obtenez la référence à la fonction à partir de son nom
        function = globals().get(self.function_name)
        if function:
            await function(*self.args, **self.kwargs)
        else:
            print(f"Function '{self.function_name}' not found.")

async def function_event_pump(event_queue):
    while True:
        event = await event_queue.get()
        await event.execute()
        event_queue.task_done()

# Démarrez la boucle d'événements
async def start_function_event_loop(event_queue):
    function_event_pump_task = asyncio.create_task(function_event_pump(event_queue))
    await function_event_pump_task