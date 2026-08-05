from app.core.exceptions import AppException

class LessonLogNotFound(AppException):
    status_code = 404
    detail = "Запись о занятии не найдена."


class LessonLogForStudentNotFound(AppException):
    status_code = 404
    detail = "У ученика нет записей о занятиях."