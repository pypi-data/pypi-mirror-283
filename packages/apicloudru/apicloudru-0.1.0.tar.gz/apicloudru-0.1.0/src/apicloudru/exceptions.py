class ApiSuspended(Exception):
    def __init__(self):
        self.message = "Работа этого API временно приостановлена. Мы уже в курсе проблемы и занимаемся решением. "
        super().__init__(self.message)


class TokenTehBlock(Exception):
    def __init__(self):
        self.message = ("Установлена техническая блокировка токена. Включить или выключить можно самостоятельно в "
                        "настройках безопасности.")
        super().__init__(self.message)


class TokenBlockedByQS(Exception):
    def __init__(self):
        self.message = "Ваш токен заблокирован службой качества. Свяжитесь с технической поддержкой"
        super().__init__(self.message)


class TestTimeOff(Exception):
    def __init__(self):
        self.message = "Закончился период тестирования"
        super().__init__(self.message)


class DateError(Exception):
    def __init__(self):
        self.message = "Ошибка значения переданной даты"
        super().__init__(self.message)


class MissingRequiredParameter(Exception):
    def __init__(self, parameter: str):
        self.message = f"Отсутствует параметр {parameter} или указан неверно."
        super().__init__(self.message)


class TypeIdNotCorrect(Exception):
    def __init__(self):
        self.message = "Параметр typeid не корректен, смотрите доступный список в документации"
        super().__init__(self.message)


class ParameterConflict(Exception):
    def __init__(self):
        self.message = ("Вы указали параметры, которые конфликтуют между собой. Например VIN и regNumber. Необходимо "
                        "указать либо VIN либо regNumber, что-то одно.")
        super().__init__(self.message)


class IpNotRegisteredInTheSystem(Exception):
    def __init__(self):
        self.message = "Сработала защита IP. Текущий IP не совпадает с заданным в ЛК"
        super().__init__(self.message)


class TimeMaxConnect(Exception):
    def __init__(self):
        self.message = "Достигнуто максимальное количество коннектов, при которых ресурс не вернул результата. Повторите попытку позже."
        super().__init__(self.message)


class MaxLimit(Exception):
    def __init__(self):
        self.message = "Превышено количество одновременных соединений (потоки)"
        super().__init__(self.message)


class NoRequiredParameters(Exception):
    def __init__(self):
        self.message = "Отсутствуют обязательные параметры"
        super().__init__(self.message)


class TokenNoMoney(Exception):
    def __init__(self):
        self.message = "Для выполнения запроса недостаточно средств, пополните баланс."
        super().__init__(self.message)


class WrongTokenKey(Exception):
    def __init__(self):
        self.message = "Вы указали значение параметра token в неверном формате, ключ должен содержать 32 символа."
        super().__init__(self.message)


class MissingRequiredTypeParameter(Exception):
    def __init__(self):
        self.message = "Отсутствует параметр type"
        super().__init__(self.message)


class MissingRequiredTokenParameter(Exception):
    def __init__(self):
        self.message = "Отсутствует параметр token"
        super().__init__(self.message)


class TokenNotRegisteredInTheSystem(Exception):
    def __init__(self):
        self.message = "Переданный токен не зарегистрирован в системе"
        super().__init__(self.message)


class TokenLockedInTheSystem(Exception):
    def __init__(self):
        self.message = "Переданный токен заблокирован службой качества / автоматической системой"
        super().__init__(self.message)


class TokenNoAccess(Exception):
    def __init__(self):
        self.message = "Нет доступа к запрашиваему методу запроса"
        super().__init__(self.message)


class MissingMandatoryParameter(Exception):
    def __init__(self):
        self.message = "Отсутствуют обязательные параметры"
        super().__init__(self.message)


class ForbiddenSymbolsPresent(Exception):
    def __init__(self):
        self.message = "В переменной ИМЯ присутствуют запрещенные символы"
        super().__init__(self.message)
