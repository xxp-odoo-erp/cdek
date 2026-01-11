from __future__ import annotations

import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Literal

import requests  # type: ignore

from cdek import constants
from cdek.exceptions import CdekAuthException, CdekRequestException

if TYPE_CHECKING:
    from cdek.client import CdekClient


class App:
    """Базовый класс для всех приложений API CDEK"""

    def __init__(self, client: CdekClient):
        """Сохранить клиент и подготовить HTTP-сессию"""
        self.client = client
        self.constants = constants
        self.token = None
        self.expire = 0
        self._response_headers: dict[str, str] = {}
        self._session = requests.Session()

    def _prepare_data(self, params: Any) -> dict[str, Any] | None:
        """Подготовка параметра для запроса"""
        if params is None:
            return None
        return (
            params.model_dump(exclude_none=True)
            if hasattr(params, "model_dump")
            else params
        )

    def _prepare_header(self, url: str) -> dict[str, str]:
        """Сформировать заголовки запроса с учётом типа ответа"""
        headers = {"Authorization": f"Bearer {self.token}"}

        if ".pdf" in url:
            headers["Accept"] = "application/pdf"
        else:
            headers["Accept"] = "application/json"

        return headers

    def _request(
        self,
        method: Literal["GET", "POST", "PATCH", "DELETE"],
        url: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Выполнить HTTP-запрос к API CDEK

        Args:
            method: HTTP-метод запроса
            url: относительный путь до ресурса API
            params: параметры строки запроса
            json: тело запроса в формате JSON
            **kwargs: дополнительные параметры `requests.Session.request`

        Returns:
            dict | bytes: JSON-ответ API либо содержимое файла

        Raises:
            CdekRequestException: при сетевых ошибках или ошибках API
        """
        headers = self._prepare_header(url)
        response_json = None
        try:
            response = self._session.request(
                method,
                url=f"{self.client.base_url}{url}",
                params=params,
                json=json,
                headers=headers,
                timeout=self.client.timeout,
                **kwargs,
            )
            if ".pdf" in url and response.status_code == 200:
                return response.content

            response_json = response.json()
            self._check_errors(url, response, response_json)
            self._response_headers = response.headers
            return response_json

        except requests.exceptions.RequestException as e:
            raise CdekRequestException(
                f"Ошибка сети при вызове метода {url}: {str(e)}", response=response_json
            ) from e

        except Exception as e:
            raise CdekRequestException(
                f"Ошибка при вызове метода {url}: {str(e)}"
            ) from e

    def _http_method(
        self,
        method: Literal["GET", "POST", "PATCH", "DELETE"],
        url: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Преобразовать данные и выполнить запрос с авторизацией

        Args:
            method: используемый HTTP-метод
            url: относительный путь до ресурса API
            params: объект с параметрами запроса
            json: объект, представляющий тело запроса
            **kwargs: дополнительные параметры передачи в `_request`

        Returns:
            dict | bytes: ответ API в зависимости от вызываемого метода
        """
        params = self._prepare_data(params)
        json = self._prepare_data(json)

        # Авторизуемся или получаем данные из кэша
        if not self._check_saved_token():
            self._authorize()

        return self._request(method, url, params, json, **kwargs)

    def _get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Обёртка над `_http_method` для выполнения GET-запроса"""
        return self._http_method("GET", url, params, json, **kwargs)

    def _post(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Обёртка над `_http_method` для выполнения POST-запроса"""
        return self._http_method("POST", url, params, json, **kwargs)

    def _patch(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Обёртка над `_http_method` для выполнения PATCH-запроса"""
        return self._http_method("PATCH", url, params, json, **kwargs)

    def _delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Обёртка над `_http_method` для выполнения DELETE-запроса"""
        return self._http_method("DELETE", url, params, json, **kwargs)

    def _authorize(self) -> bool:
        """
        Авторизация клиента в сервисе Интеграции

        Raises:
            CdekAuthException: в случае ошибки авторизации
        """
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client.account,
            "client_secret": self.client.secure,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = self._session.post(
                f"{self.client.base_url}oauth/token",
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

    def _save_token(self, callback: Callable[[dict[str, Any]], None]) -> None:
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
        self, method: str, response: requests.Response, api_response: dict[str, Any]
    ) -> None:
        """
        Проверить ответ на ошибки

        Args:
            method: URL метода
            response: HTTP ответ
            api_response: распарсенный JSON ответ

        Raises:
            CdekRequestException: в случае ошибки
        """

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
                    api_response,
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
                api_response,
            )

        # Общая ошибка при неверном статусе
        if response.status_code > 202 and "requests" not in api_response:
            raise CdekRequestException(
                f"Неверный код ответа от сервера CDEK при вызове метода "
                f"{method}: {response.status_code}",
                response.status_code,
                api_response,
            )
