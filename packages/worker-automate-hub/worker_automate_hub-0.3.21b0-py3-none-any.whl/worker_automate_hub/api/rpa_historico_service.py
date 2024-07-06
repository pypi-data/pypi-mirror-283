import aiohttp
from aiohttp import ClientSession

from worker_automate_hub.models.dto.rpa_hitorico_dto import RpaHistoricoDTO
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger


class RpaHistoricoService:
    def __init__(self) -> None:
        self.session: ClientSession = None

    async def __aenter__(self):
        self.session = await aiohttp.ClientSession().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
        self.session = None

    async def _send_request(self, method: str, endpoint: str, data: RpaHistoricoDTO) -> dict:
        env_config = load_env_config()
        url = f"{env_config["API_BASE_URL"]}{endpoint}"
        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}       
        payload = data.model_dump_json(by_alias=True, exclude_none=True, exclude_unset=True)
        print(f"\nPayload: {payload}")

        try:
            async with self.session.request(method, url, data=payload, headers=headers_basic) as response:
                response_text = await response.text()
                logger.info(f"Resposta {method} {endpoint}: {response_text}")

                if response.status == 200:
                    try:
                        response_data = await response.json()
                        return {
                            "success": response_data,
                            "status_code": response.status,
                        }
                    except aiohttp.ContentTypeError:
                        return {
                            "error": "Resposta não é JSON",
                            "status_code": response.status,
                        }
                else:
                    return {"error": response_text, "status_code": response.status}

        except aiohttp.ClientError as e:
            logger.error(f"Erro de cliente aiohttp em {method} {endpoint}: {str(e)}")
            return {"error": str(e), "status_code": 500}
        except Exception as e:
            logger.error(f"Erro inesperado em {method} {endpoint}: {str(e)}")
            return {"error": str(e), "status_code": 500}

    async def store(self, data: RpaHistoricoDTO) -> dict:
        return await self._send_request("POST", "/historico", data)

    async def update(self, uuid_historico: str, data: RpaHistoricoDTO) -> dict:
        return await self._send_request("PUT", f"/historico", data)
