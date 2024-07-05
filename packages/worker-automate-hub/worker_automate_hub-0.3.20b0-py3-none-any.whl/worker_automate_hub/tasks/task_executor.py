from rich.console import Console

from worker_automate_hub.tasks.task_definitions import task_definitions
from worker_automate_hub.utils.logger import logger

console = Console()


async def perform_task(task):
    try:
        console.print(
            f"\nProcesso a ser executado: {task['nomProcesso']}\n", style="green"
        )
        logger.info(f"Processo a ser executado: {task['nomProcesso']}")
        task_uuid = task["uuidProcesso"]
        if task_uuid in task_definitions:
            result = await task_definitions[task_uuid](task)
            return result
        else:
            console.print(f"Processo não encontrado: {task_uuid}", style="yellow")
            logger.error(f"Processo não encontrado: {task_uuid}")
            return None
    except Exception as e:
        console.print(f"Erro ao performar o processo: {e}\n", style="red")
        logger.error(f"Erro ao performar o processo: {e}")
