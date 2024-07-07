import aiohttp

from .client import execute_get, construct_url, APIService
from .models.fssp import FSSPPhysicalSearch


class ApiCloudRu:
    def __init__(self, token):
        self._token = token
        self.root_url = 'https://api-cloud.ru/api/'
        self.FSSP = self._FSSP(self)
        self.LK = self._LK(self)

    class _FSSP:
        def __init__(self, parent):
            self.parent: ApiCloudRu = parent

        async def get_physical(self, lastname: str,
                               firstname: str,
                               second_name: str,
                               birthdate: str,
                               region: int = -1,
                               only_actual: bool = 1) -> FSSPPhysicalSearch:
            res = await execute_get(self.parent.root_url,
                                    APIService.fssp,
                                    self.parent._token,
                                    type='physical',
                                    lastname=lastname,
                                    firstname=firstname,
                                    birthdate=birthdate,
                                    region=region,
                                    only_actual=only_actual,
                                    second_name=second_name
                                    )
            return FSSPPhysicalSearch.parse_obj(res)

    class _LK:
        def __init__(self, parent):
            self.parent: ApiCloudRu = parent

        async def get_balance(self):
            return await execute_get(self.parent.root_url,
                                     APIService.lk,
                                     self.parent._token,
                                     type='balance')

        # async def get_api_status
