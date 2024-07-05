import asyncio
import math
import os
import subprocess
import numpy as np
import cv2
import psutil
import pyautogui
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog
from rich.console import Console

from worker_automate_hub.config.settings import (
    load_env_config,
    load_worker_config,
)
from worker_automate_hub.utils.logger import logger

console = Console()


async def get_system_info():
    worker_config = load_worker_config()
    max_cpu = psutil.cpu_percent(interval=10.0)
    cpu_percent = psutil.cpu_percent(interval=1.0)
    memory_info = psutil.virtual_memory()

    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "maxCpu": f"{max_cpu}",
        "maxMem": f"{memory_info.total / (1024 ** 3):.2f}",
        "usoCpu": f"{cpu_percent}",
        "usoMem": f"{memory_info.used / (1024 ** 3):.2f}",
        "situacao": "{'status': 'em desenvolvimento'}",
    }


async def get_new_task_info():
    env_config = load_env_config()
    worker_config = load_worker_config()
    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "versao": env_config["VERSION"],
    }


def multiselect_prompt(options, title="Select options"):
    result = checkboxlist_dialog(
        values=[(option, option) for option in options],
        title=title,
        text="Use space to select multiple options.\nPress Enter to confirm your selection.",
    ).run()

    if result is None:
        console.print("[red]No options selected.[/red]")
    else:
        return result


def select_prompt(options, chave_1, title="Selecione uma opção"):
    values = [(index, option[chave_1]) for index, option in enumerate(options)]

    result = radiolist_dialog(
        values=values,
        title=title,
        text="Use as teclas de seta para navegar e Enter para selecionar uma opção.",
    ).run()

    if result is None:
        console.print("[red]Nenhuma opção selecionada.[/red]")
    else:
        # Retorna o dicionário correspondente ao índice selecionado
        return options[result]


async def kill_process(process_name: str):
    try:
        # Obtenha o nome do usuário atual
        current_user = os.getlogin()

        # Liste todos os processos do sistema
        result = await asyncio.create_subprocess_shell(
            f'tasklist /FI "USERNAME eq {current_user}" /FO CSV /NH',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            logger.error(f"Erro ao listar processos: {stderr.decode().strip()}", None)
            console.print(
                f"Erro ao listar processos: {stderr.decode().strip()}", style="bold red"
            )
            return

        if stdout:
            lines = stdout.decode().strip().split("\n")
            for line in lines:
                # Verifique se o processo atual corresponde ao nome do processo
                if process_name in line:
                    try:
                        # O PID é a segunda coluna na saída do tasklist
                        pid = int(line.split(",")[1].strip('"'))
                        await asyncio.create_subprocess_exec(
                            "taskkill", "/PID", str(pid), "/F"
                        )
                        # logger.info(
                        #     f"Processo {process_name} (PID {pid}) finalizado.", None
                        # )
                        console.print(
                            f"\nProcesso {process_name} (PID {pid}) finalizado.\n",
                            style="bold green",
                        )
                    except Exception as ex:
                        # logger.error(
                        #     f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}",
                        #     None,
                        # )
                        console.print(
                            f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}",
                            style="bold red",
                        )
        else:
            logger.info(
                f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}.",
                None,
            )
            console.print(
                f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}.",
                style="bold yellow",
            )

    except Exception as e:
        logger.error(f"Erro ao tentar matar o processo: {e}", None)
        console.print(f"Erro ao tentar matar o processo: {e}", style="bold red")


async def find_element_center(image_path, region_to_look, timeout):
    try:
        counter = 0
        confidence_value = 1.00
        grayscale_flag = False

        while counter <= timeout:
            try:
                element_center = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region_to_look,
                    confidence=confidence_value,
                    grayscale=grayscale_flag,
                )
            except Exception as ex:
                element_center = None
                # logger.info(str(ex), None)
                # console.print(
                #     f"Erro em locateCenterOnScreen: {str(ex)}", style="bold red"
                # )
                console.print(f"Elemento náo encontrado na pos: {region_to_look}")

            if element_center:
                return element_center
            else:
                counter += 1

                if confidence_value > 0.81:
                    confidence_value -= 0.01

                if counter >= math.ceil(timeout / 2):
                    grayscale_flag = True

                await asyncio.sleep(1)

        return None
    except Exception as ex:
        # logger.info(str(ex), None)
        # console.print(f"Erro em find_element_center: {str(ex)}", style="bold red")
        console.print(f"{counter} - Buscando elemento na tela: {region_to_look}", style="bold yellow")
        return None
    
async def find_element_center_old_2(image_path, region_to_look, timeout):
    counter = 0
    confidence_value = 1.00
    grayscale_flag = False

    while counter <= timeout:
        try:
            element_center = pyautogui.locateCenterOnScreen(
                image_path,
                region=region_to_look,
                confidence=confidence_value,
                grayscale=grayscale_flag,
            )

            if element_center:
                return element_center

            counter += 1
            if confidence_value > 0.81:
                confidence_value -= 0.01

            if counter >= math.ceil(timeout / 2):
                grayscale_flag = True

            await asyncio.sleep(1)

        except Exception as ex:
            # logger.info(f"Erro ao localizar a imagem: {str(ex)}", None)
            console.print(f"{counter} - Buscando elemento na tela: {region_to_look}", style="bold yellow")

    logger.info(f"Imagem {image_path} não encontrada na região especificada.", None)
    console.print(f"Imagem {image_path} não encontrada na região especificada.", style="bold red")
    return None

async def find_element_center_last(image_path, region_to_look, timeout):
    screen_width, screen_height = pyautogui.size()
    console.print(f"Bunscando a imagem: {image_path}")

    counter = 0
    confidence_value = 1.00
    grayscale_flag = False
    image = cv2.imread(image_path)
    image_height, image_width = image.shape[:2]
    region_step = max(image_width, image_height)  # Define o tamanho das regiões a serem pesquisadas
    regions = [
        (x, y, region_step, region_step)
        for x in range(0, screen_width, region_step)
        for y in range(0, screen_height, region_step)
    ]

    while counter <= timeout:
        for region in regions:
            try:
                element_center = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region,
                    confidence=confidence_value,
                    grayscale=grayscale_flag,
                )

                if element_center:
                    console.print(f"Elemento encontrado: {element_center}", style="bold green")
                    x, y = element_center
                    # Draw a rectangle on the screen indicating the position
                    screenshot = pyautogui.screenshot()
                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    cv2.rectangle(screenshot, (x-50, y-50), (x+50, y+50), (0, 255, 0), 2)
                    cv2.imshow('Detected Element', screenshot)
                    cv2.waitKey(5000)  # Display for 5 seconds
                    cv2.destroyAllWindows()
                    return element_center

            except Exception as ex:
                # logger.info(f"Erro ao localizar a imagem: {str(ex)}", None)
                console.print(f"{counter} - Buscando elemento na região: {region}", style="bold yellow")

        counter += 1
        if confidence_value > 0.81:
            confidence_value -= 0.01

        if counter >= math.ceil(timeout / 2):
            grayscale_flag = True

        await asyncio.sleep(1)

    logger.info(f"Imagem {image_path} não encontrada na tela.", None)
    console.print(f"Imagem {image_path} não encontrada na tela.", style="bold red")
    return None


def type_text_into_field(text, field, empty_before, chars_to_empty):
    try:
        if empty_before:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)

        field.type_keys(text, with_spaces=True)

        if str(field.texts()[0]) == text:
            return
        else:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)
            field.type_keys(text, with_spaces=True)
    except Exception as ex:
        logger.error("Erro em type_text_into_field: " + str(ex), None)
        console.print(f"Erro em type_text_into_field: {str(ex)}", style="bold red")


async def wait_element_ready_win(element, trys):
    max_trys = 0

    while max_trys < trys:
        try:
            if element.wait("exists", timeout=2):
                await asyncio.sleep(1)
                if element.wait("exists", timeout=2):
                    await asyncio.sleep(1)
                    if element.wait("enabled", timeout=2):
                        element.set_focus()
                        await asyncio.sleep(1)
                        if element.wait("enabled", timeout=1):
                            return True

        except Exception as ex:
            logger.error("wait_element_ready_win -> " + str(ex), None)
            console.print(
                f"Erro em wait_element_ready_win: {str(ex)}", style="bold red"
            )

        max_trys = max_trys + 1

    return False
