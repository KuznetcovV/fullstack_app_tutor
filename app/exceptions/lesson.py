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
    status_code = 422
    detail = "Время начала занятия должно быть раньше времени конца занятия."

class LessonDateWeekdayMismatch(AppException):
    status_code = 422
    detail = "Дата не совпадает с днем недели занятия."

class LessonAlreadyCancelled(AppException):
    status_code = 409
    detail = "На эту дату занятие уже отменено."

class CancelledLessonNotFound(AppException):
    status_code = 404
    detail = "Запись об отмененном занятии не найдена."