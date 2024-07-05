import asyncio
import importlib.metadata

from rich import emoji
from rich.console import Console
from rich.prompt import Prompt
from typer import Context, Exit, Option, Typer

from worker_automate_hub.api.client import get_workers, load_environments
from worker_automate_hub.config.settings import load_env_config, set_env_values
from worker_automate_hub.utils.updater import check_for_update
from worker_automate_hub.utils.util import select_prompt

from .core.so_manipulation import add_worker_config, write_env_config
from .worker import run_worker

console = Console()
app = Typer()

HELP_MESSAGE = """
[b]Worker[/] - Grupo Argenta

Forma de uso: [b]worker [SUBCOMANDO] [ARGUMENTOS][/]

Existem 3 subcomandos disponíveis para essa aplicação

- [b]run[/]: Inicializa o Worker na máquina atual e começa a solicitar trabalho para o orquestrador.
- [b]validate[/]: Verifica se o Worker atual está configurado corretamente e pronto para ser inicializado.
- [b]assets[/]: Realiza a limpeza e depois download na pasta assets de todos arquivos utilizado pelo worker durante execução.

[b]Exemplos de uso:[/]
 [b][blue]RUN[/][/]
    [green][b]worker[/][/] [b]run[/]

 [b][blue]VALIDATE[/][/]
    [green][b]worker[/][/] [b]validate[/]

---

[b]Help:[/]
 [b]Para mais informações[/]
    [green][b]worker[/][/] --help

 [b]Para ver a versão instalada[/]
    [green][b]worker[/][/] --version

 [b]Para gerar o arquivo de configuração[/]
    [green][b]worker[/][/] --configure

 [b]Para informações detalhadas
    [blue][link=https://github.com/SIM-Rede/worker-automate-hub]Repo no GIT Argenta[/][/] | [blue][link=https://pypi.org/project/worker-automate-hub/]Publicação no PyPI[/][/]
"""


def function_help(flag: bool):
    if flag:
        console.print(
            importlib.metadata.version("worker-automate-hub"),
            style="bold blue",
        )
        raise Exit(code=0)


def function_configure(flag: bool):

    if flag:
        environment_names = [
            "teste",
            "teste-qa",
            "local",
            "dev",
            "stg",
            "main",
        ]
        chosen_environment = Prompt.ask(
            "Selecione o ambiente", choices=environment_names
        )
        env_sel = load_environments(chosen_environment)
        write_env_config(env_sel)
        env_config = load_env_config()
        set_env_values(env_config)
        workers = asyncio.run(get_workers())
        # worker_sel = select_prompt(
        #     workers, "nomRobo", title="Selecione o Worker a ser configurado"
        # )
        print(workers)
        if len(workers) == 0:
            print("Nenhum worker encontrado.")
            return
        nomes_workers = [worker["nomRobo"] for worker in workers]
        sel = Prompt.ask("Selecione um Worker", choices=nomes_workers)
        worker_sel = next(worker for worker in workers if worker["nomRobo"] == sel)
        add_worker_config(worker_sel)

        raise Exit(code=0)


def function_teste(flag: bool):

    if flag:
        load_environments("teste")


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(False, callback=function_help, is_flag=True),
    configure: bool = Option(False, callback=function_configure, is_flag=True),
    teste: bool = Option(False, callback=function_teste, is_flag=True),
):
    if ctx.invoked_subcommand:
        return
    console.print(HELP_MESSAGE)


@app.command()
def run():
    asyncio.run(run_worker())


@app.command()
def update():
    check_for_update()
