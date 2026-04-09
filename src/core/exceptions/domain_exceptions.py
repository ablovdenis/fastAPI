class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' не найден"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(login=login)

        super().__init__(detail=self._exception_text_template)


class UserLoginIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' уже существует"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(login=login)

        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundException(BaseDomainException):
    _exception_text_template = "Категория с id='{id}' не найдена"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class CategoryIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория с id='{id}' уже существует"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)