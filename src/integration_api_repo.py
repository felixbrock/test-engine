from typing import Union
import requests

from i_integration_api_repo import IIntegrationApiRepo
from snowflake_query_result_dto import SnowflakeQueryResultDto
import logging
from config import getIntegrationApiRoot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class IntegrationApiRepo(IIntegrationApiRepo):
    def __init__(self) -> None:
        self._version = 'v1'
        self._apiRoot = getIntegrationApiRoot()

    def querySnowflake(self, query: str, jwt: str, targetOrgId: Union[str, None]) -> SnowflakeQueryResultDto:
        data: "dict[str, Union[str, None]]" = {'query': query}

        data['targetOrgId'] = targetOrgId if targetOrgId else None

        response = requests.post(f'{self._apiRoot}/api/{self._version}/snowflake/query',
                                 data=data, headers={'Authorization': f'Bearer {jwt}'})
        jsonPayload = response.json()
        if response.status_code == 201:
            return SnowflakeQueryResultDto(jsonPayload)
        raise Exception(
            jsonPayload['message'] if jsonPayload['message'] else 'Unknown Error')
