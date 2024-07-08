import enum
import urllib.parse
import aiohttp
import json

from aiohttp import ClientTimeout

from .exceptions import *


class APIService(enum.Enum):
    fssp = 'fssp.php?'
    lk = 'apilk.php?'


def construct_url(root: str, token: str, **kwargs):
    kwargs['token'] = token
    return root + urllib.parse.urlencode({**kwargs})


def raise_error(error_code: int):
    match error_code:
        case 888:
            raise ForbiddenSymbolsPresent
        case 766:
            raise MissingMandatoryParameter
        case 602:
            raise TokenNoAccess
        case 504:
            raise TokenLockedInTheSystem
        case 503:
            raise TokenNotRegisteredInTheSystem
        case 502:
            raise MissingRequiredTokenParameter
        case 500:
            raise MissingRequiredTypeParameter
        case 499:
            raise WrongTokenKey
        case 498:
            raise TokenNoMoney
        case 460:
            raise NoRequiredParameters
        case 456:
            raise MaxLimit
        case 404:
            raise TimeMaxConnect
        case 123:
            raise IpNotRegisteredInTheSystem
        case 111:
            raise ParameterConflict
        case 107:
            raise TypeIdNotCorrect
        case 106:
            raise MissingRequiredParameter('number')
        case 105:
            raise MissingRequiredParameter('nameLegal')
        case 104:
            raise MissingRequiredParameter('birthdate')
        case 103:
            raise MissingRequiredParameter('region')
        case 102:
            raise MissingRequiredParameter('number')
        case 101:
            raise MissingRequiredParameter('lastname')
        case 100:
            raise MissingRequiredParameter('firstname')
        case 15:
            raise DateError
        case 5:
            raise TestTimeOff
        case 3:
            raise TokenBlockedByQS
        case 2:
            raise TokenTehBlock
        case 1:
            raise ApiSuspended


async def execute_get(root: str,
                      service: APIService,
                      token: str,
                      timeout: int = 400,
                      **kwargs,
                      ) -> dict:
    base_url = f'{root}{service.value}'
    constructed_url = construct_url(base_url, token, **kwargs)
    async with aiohttp.ClientSession(timeout=ClientTimeout(total=450)) as session:
        res = await session.get(constructed_url)
        j = json.loads(await res.text())
        if 'error' in j:
            raise_error(int(j['error']))
        return j
