from __future__ import annotations

import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import requests

from cdek import constants
from cdek.exceptions import CdekAuthException, CdekRequestException

if TYPE_CHECKING:
    from cdek.client import CdekClient


class App:
    def __init__(self, client: CdekClient):
        self.client = client
        self.constants = constants
        self._session = requests.Session()

    def _api_request(
        self, method: str, url: str, params: Any | None = None
    ) -> dict | bytes:
        """
        Выполнить запрос к API

        Args:
            method: Метод запроса (GET, POST, PATCH, DELETE)
            url: URL path запроса
            params: параметры запроса

        Returns:
            ответ от API

        Raises:
            CdekRequestException: в случае ошибки запроса
        """
        # Авторизуемся или получаем данные из кэша
        if not self._check_saved_token():
            self._authorize()

        # Проверяем является ли запрос на файл pdf
        is_pdf_file_request = ".pdf" in url

        headers = {"Authorization": f"Bearer {self.token}"}

        if is_pdf_file_request:
            headers["Accept"] = "application/pdf"
        else:
            headers["Accept"] = "application/json"

        # Подготовка параметров
        if params is not None:
            if hasattr(params, "prepare_request"):
                request_params = params.prepare_request()
            elif isinstance(params, dict):
                request_params = params
            elif hasattr(params, "model_dump"):
                # Pydantic model - convert to dict
                request_params = params.model_dump(exclude_none=True)
            else:
                request_params = params
        else:
            request_params = None

        try:
            if method == "GET":
                response = self._session.get(
                    f"{self.client.base_url}{url}",
                    params=request_params,
                    headers=headers,
                    timeout=self.client.timeout,
                )
            elif method == "POST":
                response = self._session.post(
                    f"{self.client.base_url}{url}",
                    json=request_params,
                    headers=headers,
                    timeout=self.client.timeout,
                )
            elif method == "PATCH":
                response = self._session.patch(
                    f"{self.client.base_url}{url}",
                    json=request_params,
                    headers=headers,
                    timeout=self.client.timeout,
                )
            elif method == "DELETE":
                response = self._session.delete(
                    f"{self.client.base_url}{url}",
                    headers=headers,
                    timeout=self.client.timeout,
                )
            else:
                raise ValueError(f"Неподдерживаемый метод: {method}")

            # Если запрос на PDF
            if is_pdf_file_request:
                if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "")
                    if "application/pdf" in content_type:
                        return response.content
                # Если не PDF, продолжаем обработку как обычный ответ

            # Парсим JSON ответ
            api_response = response.json()

            # Проверяем ошибки
            self._check_errors(url, response, api_response)

            # Возвращаем PDF если это PDF запрос
            if is_pdf_file_request and response.status_code == 200:
                return response.content

            return api_response

        except requests.exceptions.RequestException as e:
            raise CdekRequestException(
                f"Ошибка сети при вызове метода {url}: {str(e)}"
            ) from e

    def _authorize(self) -> bool:
        """
        Авторизация клиента в сервисе Интеграции

        Raises:
            CdekAuthException: в случае ошибки авторизации
        """
        params = {
            constants.AUTH_KEY_TYPE: constants.AUTH_PARAM_CREDENTIAL,
            constants.AUTH_KEY_CLIENT_ID: self.client.account,
            constants.AUTH_KEY_SECRET: self.client.secure,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = self._session.post(
                f"{self.client.base_url}{constants.OAUTH_URL}",
                data=params,
                headers=headers,
                timeout=self.client.timeout,
            )

            if response.status_code == 200:
                token_info = response.json()
                self.token = token_info.get("access_token", "")
                expires_in = token_info.get("expires_in", 0)
                self.expire = int(time.time()) + expires_in - 10

                if self.client.memory_save_callback is not None:
                    self._save_token(self.client.memory_save_callback)

                return True
            else:
                raise CdekAuthException(constants.AUTH_FAIL)

        except requests.exceptions.RequestException as e:
            raise CdekAuthException(f"{constants.AUTH_FAIL}: {str(e)}") from e

    def _check_saved_token(self) -> bool:
        """Проверить сохранённый токен"""
        check_memory = self.client.memory

        # Если не передан верный сохранённый массив данных для авторизации
        if (
            not check_memory
            or "account_type" not in check_memory
            or "expires_in" not in check_memory
            or "access_token" not in check_memory
        ):
            return False

        # Проверяем тип аккаунта
        if check_memory.get("account_type") != self.client.account_type:
            return False

        # Проверяем срок действия токена
        if check_memory["expires_in"] > time.time() and check_memory.get(
            "access_token"
        ):
            self.token = check_memory["access_token"]
            return True

        return False

    def _save_token(self, callback: Callable):
        """Сохранить токен через коллбэк"""
        callback(
            {
                "cdekAuth": {
                    "expires_in": self.expire,
                    "access_token": self.token,
                    "account_type": self.client.account_type,
                }
            }
        )

    def _check_errors(
        self, method: str, response: requests.Response, api_response: dict
    ):
        """
        Проверить ответ на ошибки

        Args:
            method: URL метода
            response: HTTP ответ
            api_response: распарсенный JSON ответ

        Raises:
            CdekRequestException: в случае ошибки
        """
        if not api_response:
            raise CdekRequestException(
                f"От API CDEK при вызове метода {method} пришел пустой ответ",
                response.status_code,
            )

        # Обработка ошибок с requests
        if response.status_code > 202 and "requests" in api_response:
            if (
                "errors" in api_response["requests"][0]
                or api_response["requests"][0].get("state") == "INVALID"
            ):
                error_data = api_response["requests"][0]["errors"][0]
                message = CdekRequestException.get_translation(
                    error_data["code"], error_data["message"]
                )
                raise CdekRequestException(
                    f"От API CDEK при вызове метода {method} "
                    f"получена ошибка: {message}",
                    response.status_code,
                )

        # Обработка общих ошибок
        if isinstance(api_response, dict) and (
            ("errors" in api_response and response.status_code == 200)
            or (api_response.get("state") == "INVALID")
            or ("errors" in api_response and response.status_code != 200)
        ):
            error_data = api_response["errors"][0]
            message = CdekRequestException.get_translation(
                error_data["code"], error_data["message"]
            )
            raise CdekRequestException(
                f"От API CDEK при вызове метода {method} получена ошибка: {message}",
                response.status_code,
            )

        # Общая ошибка при неверном статусе
        if response.status_code > 202 and "requests" not in api_response:
            raise CdekRequestException(
                f"Неверный код ответа от сервера CDEK при вызове метода "
                f"{method}: {response.status_code}",
                response.status_code,
            )
