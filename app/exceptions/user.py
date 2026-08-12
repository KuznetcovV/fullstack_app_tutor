from app.core.exceptions import AppException

class UserNotFound(AppException):
    status_code = 404
    detail = "Пользователь не найден"