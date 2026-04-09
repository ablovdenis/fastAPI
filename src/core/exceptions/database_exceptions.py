class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class UserNotFoundException(BaseDatabaseException):
    pass


class UserAlreadyExistsException(BaseDatabaseException):
    pass


class CategoryNotFoundException(BaseDatabaseException):
    pass


class CategiryAlreadyExistsException(BaseDatabaseException):
    pass


class LocationNotFoundException(BaseDatabaseException):
    pass


class LocationAlreadyExistsException(BaseDatabaseException):
    pass


class PostNotFoundException(BaseDatabaseException):
    pass


class CommentNotFoundException(BaseDatabaseException):
    pass