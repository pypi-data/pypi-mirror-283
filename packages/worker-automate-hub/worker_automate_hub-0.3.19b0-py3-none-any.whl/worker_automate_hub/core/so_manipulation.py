import os

import toml
from pathlib3x import Path


def write_env_config(env: tuple):
    try:
        env_dict = env[0]
        home_dir = Path(os.path.expanduser("~"))
        config_path = home_dir / "worker-automate-hub"
        config_path.mkdir(exist_ok=True)
        assets_path = config_path / "assets"
        logs_path = config_path / "logs"
        assets_path.mkdir(exist_ok=True)
        logs_path.mkdir(exist_ok=True)

        config_file_path = config_path / "settings.toml"
        config_data = {
            "name": "WORKER",
            "params": {
                "api_base_url": env_dict["API_BASE_URL"],
                "api_auth": env_dict["API_AUTHORIZATION"],
                "notify_alive_interval": env_dict["NOTIFY_ALIVE_INTERVAL"],
                "version": env_dict["VERSION"],
                "log_level": env_dict["LOG_LEVEL"],
            },
        }
        with open(
            config_file_path, "w"
        ) as config_file:  # Use "w" mode to write or overwrite
            toml.dump(config_data, config_file)
            print(f"Arquivo de configuração criado em: {config_file_path}")

        return {
            "Message": f"Arquivo de configuração do ambiente criado em {config_path}",
            "Status": True,
        }
    except Exception as e:
        return {
            "Message": f"Erro ao criar o arquivo de configuração do ambiente.\n Comando retornou: {e}",
            "Status": False,
        }


def add_worker_config(worker):
    try:
        home_dir = Path(os.path.expanduser("~"))
        config_file_path = home_dir / "worker-automate-hub" / "settings.toml"

        if not config_file_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_file_path}")

        with open(config_file_path, "r") as config_file:
            config_data = toml.load(config_file)

        config_data["id"] = {
            "worker_uuid": worker["uuidRobo"],
            "worker_name": worker["nomRobo"],
        }

        with open(config_file_path, "w") as config_file:
            toml.dump(config_data, config_file)

        return {
            "Message": f"Informações do worker adicionadas ao arquivo de configuração em {config_file_path}",
            "Status": True,
        }
    except Exception as e:
        return {
            "Message": f"Erro ao adicionar informações do worker ao arquivo de configuração.\n Comando retornou: {e}",
            "Status": False,
        }


# def make_configuration_file(worker, env) -> dict:
#     try:
#         home_dir = Path(os.path.expanduser('~'))
#     except Exception as e:
#         erro = f'Erro ao obter o diretório HOME.\n Comando retornou: {e}'
#         return {'Message': erro, 'Status': False}

#     try:
#         config_path = home_dir / 'worker-automate-hub'
#         config_path.mkdir(exist_ok=True)
#         assets_path = config_path / 'assets'
#         logs_path = config_path / 'logs'
#         assets_path.mkdir(exist_ok=True)
#         logs_path.mkdir(exist_ok=True)

#         config_file_path = config_path / 'settings.toml'
#         config_file_path.touch(exist_ok=True)
#         with open(config_file_path, 'w+') as config_file:
#             config_file.write(
#                 f'name = "WORKER"\n\n'
#                 f'[id]\nworker_uuid = "{worker["uuidRobo"]}"\nworker_name = "{worker["nomRobo"]}"\n\n'
#                 f'[params]\napi_base_url = "{env['API_BASE_URL']}"\napi_auth = "{env['API_AUTHORIZATION']}"\nnotify_alive_interval = {env['NOTIFY_ALIVE_INTERVAL']}\nversion = "{env['VERSION']}"\nlog_level = "{env['LOG_LEVEL']}"'
#             )

#         retorno = {
#             'Message': f'Arquivo de configuração criado em {config_path}',
#             'Status': True,
#         }
#     except FileExistsError as e:
#         erro = f'Arquivo de configuração já criado ou pasta já existe em {home_dir}.\n Comando retornou: {e}'
#         retorno = {'Message': erro, 'Status': False}
#     except Exception as e:
#         erro = f'Ocorreu um erro ao criar o arquivo de configuração.\n Comando retornou: {e}'
#         retorno = {'Message': erro, 'Status': False}

#     return retorno


# def get_secret(
#     app: str,
#     env: str,
#     proj: str,
#     conf: str,
#     token: str,
#     vault_url: str
# ) -> dict:
#     headers = {'X-Vault-Token': token}
#     try:
#         response = requests.request(
#             'GET', url=vault_url + f'/v1/{env}-{proj}/data/{app}/{conf}', headers=headers
#         )
#     except Exception as e:
#         return {'Status': e}

#     if response.status_code == 200:
#         if conf == 'env':
#             ret = response.json()['data']['data']
#         else:
#             ret = response.json()['data']['data']['content']
#     else:
#         ret = {'Status': 'Erro'}
#     return ret

# def get_metadata(
#     app: str,
#     env: str,
#     proj: str,
#     token: str,
#     vault_url: str,
# ) -> list:
#     headers = {'X-Vault-Token': token}
#     try:
#         response = requests.request(
#             'LIST', url=vault_url + f'/v1/{env}-{proj}/metadata/{app}', headers=headers
#         )
#     except Exception as e:
#         return [f'Erro {e}']

#     if response.status_code == 200:
#         ret = response.json()['data']['keys']
#     else:
#         ret = [f'Erro', response.text]
#     return ret

# def convert_to_json(
#     file: str,
# ) -> dict:
#     with open(file, 'r') as f:
#         content = f.readlines()

#     contentList = [x.strip().split('^#')[0].split('=', 1) for x in content if '=' in x.split('^#')[0]]
#     contentDict = dict(contentList)
#     for k, v in contentList:
#         # for i, x in enumerate(v.split('$')[1:]):
#         #     key = re.findall(r'\w+', x)[0]
#         #     v = v.replace('$' + key, contentDict[key])
#         if '=' in v or '$' in v or '#' in v:
#             if "'" in v:
#                 contentDict[k] = v.strip()
#             else:
#                 contentDict[k] = f"'{v.strip()}'"
#         else:
#             contentDict[k] = v.strip()

#     return json.dumps(contentDict)

# def replace_string(secret, search, replace):
#     with open(secret, 'rt') as file_in:
#         novo_arquivo = file_in.read()

#     with open(secret, 'wt') as file_out:
#         novo_arquivo = novo_arquivo.replace(search, replace)
#         file_out.write(novo_arquivo)

# def update_secret(
#     app: str,
#     env: str,
#     proj: str,
#     secret: str,
#     token: str,
#     vault_url: str,
#     file: dict,
# ) -> dict:
#     headers = {'X-Vault-Token': token}
#     match secret:
#         case 'env':
#             json_file = Path('json_file.json')
#             json_file.touch()
#             json_file.write_text('{"data":'+file+'}')
#             payload = open('json_file.json', 'rb').read()
#             try:
#                 ret = requests.request(
#                     'POST', url=vault_url + f'/v1/{env}-{proj}/data/{app}/{secret}', headers=headers, data=payload
#                 )
#             except Exception as e:
#                 return {'Status': e}
#             json_file.unlink()
#         case _:
#             if 'env.js' in secret or 'json' in secret:
#                 replace_string(file, '\"', '\\\"')

#             with open(file, 'r') as f:
#                 content = f.readlines()
#             converted = ''
#             # contentList = [x.strip().split('#')[0].split('=', 1) for x in content if '=' in x.split('#')[0]]
#             for line in content:
#                 if converted == '':
#                     converted = f'{line}'.strip()+'\\n'
#                 else:
#                     converted = f'{converted}{line}'.strip()+'\\n'

#             json_file = Path('json_file.json')
#             json_file.touch()
#             json_file.write_text('{"data": {"content": "'+converted+'"} }')

#             payload = open('json_file.json', 'rb').read()
#             try:
#                 ret = requests.request(
#                     'POST', url=vault_url + f'/v1/{env}-{proj}/data/{app}/{secret}', headers=headers, data=payload
#                 )
#             except Exception as e:
#                 return {'Status': e}
#             json_file.unlink()

#             if 'env.js' in secret or 'json' in secret:
#                 replace_string(file, '\\\"', '\"')

#     if ret.status_code == 200:
#         return {'Status': 'Success'}
#     else:
#         return {'Status': (ret.text)}

# def get_environment(
#     token: str,
#     vault_url: str,
# ) -> dict:
#     headers = {'X-Vault-Token': token }
#     try:
#         mounts = requests.request('GET', url=vault_url + '/v1/sys/mounts', headers=headers)
#     except Exception as e:
#         retorno = {'Status': f'Erro: {e}'}

#     if mounts.status_code == 200:
#         search = ['local', 'dev', 'qa', 'main']
#         matches = []

#         for k, v in mounts.json().items():
#             if any([x in k for x in search]):
#                 matches.append(k)
#         matches.sort()

#         paths_metadata = {}
#         for path in matches:
#             paths_response = requests.request('LIST', url=f'https://aspirina.simtech.solutions/v1/{path}metadata', headers=headers)
#             if paths_response.status_code == 200:
#                 paths_metadata[path] = paths_response.json()['data']['keys']

#         retorno = paths_metadata
#     else:
#         retorno = {'Status': f'Erro: {mounts.text}'}

#     return retorno

# def query_yes_no(
#     question: str,
#     default: str
# ) -> str:
#     valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
#     if default is None:
#         prompt = " [y/n] "
#     elif default == "yes":
#         prompt = " [Y/n] "
#     elif default == "no":
#         prompt = " [y/N] "
#     else:
#         raise ValueError("invalid default answer: '%s'" % default)

#     while True:
#         stdout.write(f'{question} {prompt}')
#         choice = input().lower()
#         if default is not None and choice == "":
#             return valid[default]
#         elif choice in valid:
#             return valid[choice]
#         else:
#             stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
