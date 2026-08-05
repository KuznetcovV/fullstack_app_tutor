from app.core.exceptions import AppException

class SubscriptionNotFound(AppException):
    status_code = 404
    detail = "Абонемент не найден"

class SubscriptionActiveNotFound(AppException):
    status_code = 404
    detail = "Активных абонементов нет"

class SubscriptionsForStudentNotFound(AppException):
    status_code = 404
    detail = "У указанного ученика нет абонементов"

class SubscriptionDatesIntersection(AppException):
    status_code = 409
    detail = "Пересечение дат с существующим абонементом для этого ученика"

class ZeroLessonsForSubscriptionCreate(AppException):
    status_code = 404
    detail = "Для создания абонемента у ученика должны быть занятия в расписании"

class InvalidDatesInetvalError(AppException):
    status_code = 409
    detail = "Дата начала должна быть меньше даты конца"