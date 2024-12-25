class CustomException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DataIsNotExists(CustomException):
    def __init__(self, message: str = "Таких данных не существует!"):
        super().__init__(message)


class DataAlreadyExists(CustomException):
    def __init__(self, message: str = "Данные уже существуют"):
        super().__init__(message)


class InvalidData(CustomException):
    def __init__(self, message: str = "Некорректные данные"):
        super().__init__(message)