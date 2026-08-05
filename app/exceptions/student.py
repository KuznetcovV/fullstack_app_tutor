from app.core.exceptions import AppException

class StudentNotFound(AppException):
    status_code = 404
    detail = "Ученик не найден."


class StudentAlreadyExists(AppException):
    status_code = 409
    detail = "Такой ученик уже существует."

class StudentLessonMismatch(AppException):
    status_code = 409
    detail = "У указанного ученика нет такого занятия"