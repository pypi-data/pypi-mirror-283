import os
from importlib import metadata
from pathlib import Path

import toml
from dotenv import load_dotenv

load_dotenv(".env")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
VAULT_URL = os.environ.get("VAULT_URL")
# API_BASE_URL = os.getenv("API_BASE_URL", "")
# VERSION = os.getenv("VERSION", "")
# NOTIFY_ALIVE_INTERVAL = int(os.getenv("NOTIFY_ALIVE_INTERVAL", "60"))
# NOME_ROBO = os.getenv("NOME_ROBO", "")
# UUID_ROBO = os.getenv("UUID_ROBO", "")
# API_AUTHORIZATION = os.getenv("API_AUTHORIZATION", "")
# LOG_LEVEL = int(os.getenv("LOG_LEVEL", "30"))
API_BASE_URL = None
VERSION = None
NOTIFY_ALIVE_INTERVAL = "60"
API_AUTHORIZATION = None
LOG_LEVEL = 10
UUID_ROBO = None
NOME_ROBO = None


def get_package_version(package_name):
    try:
        version = metadata.version(package_name)
        return version
    except metadata.PackageNotFoundError:
        return "Package not found"


def load_env_config():
    try:
        home_dir = Path(os.path.expanduser("~"))
        config_file_path = home_dir / "worker-automate-hub" / "settings.toml"

        if not config_file_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado em: {config_file_path}"
            )

        with open(config_file_path, "r") as config_file:
            config = toml.load(config_file)

        # Atribuir as variáveis de configuração do ambiente
        env_config = {
            "API_BASE_URL": config["params"]["api_base_url"],
            "VERSION": config["params"]["version"],
            "NOTIFY_ALIVE_INTERVAL": config["params"]["notify_alive_interval"],
            "API_AUTHORIZATION": config["params"]["api_auth"],
            "LOG_LEVEL": config["params"]["log_level"],
        }

        return env_config

    except Exception as e:
        raise Exception(f"Erro ao carregar o arquivo de configuração do ambiente: {e}")
        # return None


def load_worker_config():
    try:
        home_dir = Path(os.path.expanduser("~"))
        config_file_path = home_dir / "worker-automate-hub" / "settings.toml"

        if not config_file_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_file_path}")

        with open(config_file_path, "r") as config_file:
            config = toml.load(config_file)

        # Atribuir as variáveis de configuração do worker
        worker_config = {
            "NOME_ROBO": config["id"]["worker_name"],
            "UUID_ROBO": config["id"]["worker_uuid"],
        }

        return worker_config

    except Exception as e:
        print(f"Erro ao carregar o arquivo de configuração do worker: {e}")
        return None


def set_env_values(env_config):
    global API_BASE_URL, VERSION, NOTIFY_ALIVE_INTERVAL, API_AUTHORIZATION, LOG_LEVEL

    API_BASE_URL = env_config["API_BASE_URL"]
    VERSION = env_config["VERSION"]
    NOTIFY_ALIVE_INTERVAL = env_config["NOTIFY_ALIVE_INTERVAL"]
    API_AUTHORIZATION = env_config["API_AUTHORIZATION"]
    LOG_LEVEL = env_config["LOG_LEVEL"]

    # print(env_config)


def set_worker_values(worker_config):
    global NOME_ROBO, UUID_ROBO
    NOME_ROBO = worker_config["NOME_ROBO"]
    UUID_ROBO = worker_config["UUID_ROBO"]


# Primeiro, carregue as configurações do ambiente
# env_config = load_env_config()
# set_env_values(env_config)

# Depois, carregue as informações do worker
# worker_config = load_worker_config()
# set_worker_values(worker_config)


# environments = {
#     "local": {
#         "API_BASE_URL": "http://127.0.0.1:3002/automate-hub",
#         "VERSION": get_package_version("worker-automate-hub"),
#         "NOTIFY_ALIVE_INTERVAL": "30",
#         "API_AUTHORIZATION": "Bearer devtoken",
#         "LOG_LEVEL": "30",
#     },
#     "dev": {
#         "API_BASE_URL": "https://dev.api.example.com",
#         "VERSION": get_package_version("worker-automate-hub"),
#         "NOTIFY_ALIVE_INTERVAL": "30",
#         "API_AUTHORIZATION": "Bearer devtoken",
#         "LOG_LEVEL": "10",
#     },
#     "stg": {
#         "API_BASE_URL": "https://staging.api.example.com",
#         "VERSION": get_package_version("worker-automate-hub"),
#         "NOTIFY_ALIVE_INTERVAL": "60",
#         "API_AUTHORIZATION": "Bearer stagingtoken",
#         "LOG_LEVEL": "20",
#     },
#     "main": {
#         "API_BASE_URL": "https://api.example.com",
#         "VERSION": get_package_version("worker-automate-hub"),
#         "NOTIFY_ALIVE_INTERVAL": "60",
#         "API_AUTHORIZATION": "Bearer prodtoken",
#         "LOG_LEVEL": "10",
#     },
# }
