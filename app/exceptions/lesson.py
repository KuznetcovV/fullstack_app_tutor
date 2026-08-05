from app.core.exceptions import AppException

class LessonNotFound(AppException):
    status_code = 404
    detail = "Занятие не найдено."

class LessonsForStudentNotFound(AppException):
    status_code = 404
    detail = "У указанного ученика нет занятий."

class LessonTimeIntersection(AppException):
    status_code = 409
    detail = "Указанное время занятия пересекается с уже существующим."

class InvalidLessonTimeInterval(AppException):
    status_code = 409
    detail = "Время начала занятия должно быть раньше времени конца занятия."