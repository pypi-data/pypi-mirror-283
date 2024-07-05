import asyncio

import pyautogui
from rich.console import Console

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    find_element_center,
    kill_process,
    type_text_into_field,
    wait_element_ready_win,
)

console = Console()


async def login_emsys(task):
    from pywinauto.application import Application  # type: ignore

    try:
        # Mata todos processos do emsys antes de abrir uma nova instancia
        kill_process("EMSys")

        # Abre um novo emsys
        app = Application().start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        console.print("EMSys iniciado.", style="bold green")

        # Testa se existe alguma mensagem no Emsys
        window_message_login_emsys = await find_element_center(
            "assets/emsys/window_message_login_emsys.png", (560, 487, 1121, 746), 35
        )

        # Clica no "Não mostrar novamente" se existir
        if window_message_login_emsys:
            pyautogui.click(window_message_login_emsys.x, window_message_login_emsys.y)
            pyautogui.click(
                window_message_login_emsys.x + 383, window_message_login_emsys.y + 29
            )
            console.print("Mensagem de login encontrada e fechada.", style="bold green")

        # Ve se o Emsys esta aberto no login
        image_emsys_login = await find_element_center(
            "assets/emsys/logo_emsys_login.png", (800, 200, 1400, 700), 600
        )
        config_robot = await get_config_by_name("Login EmSys")
        if image_emsys_login:
            await asyncio.sleep(10)
            type_text_into_field(
                config_robot["EmSys DB"], app["Login"]["ComboBox"], True, "50"
            )
            pyautogui.press("enter")
            await asyncio.sleep(2)

            if await wait_element_ready_win(app["Login"]["Edit2"], 30):
                disconect_database = await find_element_center(
                    "assets/emsys/disconect_database.png", (1123, 452, 1400, 578), 300
                )

                if disconect_database:
                    # Realiza login no Emsys
                    type_text_into_field(
                        config_robot["user EmSys"], app["Login"]["Edit2"], True, "50"
                    )
                    pyautogui.press("tab")
                    type_text_into_field(
                        config_robot["password EmSys"],
                        app["Login"]["Edit1"],
                        True,
                        "50",
                    )
                    pyautogui.press("enter")

                    # Seleciona a filial do emsys
                    selecao_filial = await find_element_center(
                        "assets/emsys/selecao_filial.png", (480, 590, 820, 740), 350
                    )

                    if selecao_filial:
                        type_text_into_field(
                            task["filial"],
                            app["Seleção de Empresas"]["Edit"],
                            True,
                            "50",
                        )
                        pyautogui.press("enter")

                        button_logout = await find_element_center(
                            "assets/emsys/button_logout.png", (0, 0, 130, 150), 750
                        )

                        if button_logout:
                            console.print(
                                "Login realizado com sucesso.", style="bold green"
                            )
                            return app
            else:
                logger.info("login_emsys_win -> wait_element_ready_win [1]", None)
                console.print("Elemento de login não está pronto.", style="bold red")

    except Exception as ex:
        logger.error("Erro em login_emsys: " + str(ex), None)
        console.print(f"Erro em login_emsys: {str(ex)}", style="bold red")

    return None
