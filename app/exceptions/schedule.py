from app.core.exceptions import AppException

class ScheduleDateFromAfterDateTo(AppException):
    status_code = 422
    detail = "Дата конца промежутка не может быть меньше даты начала."

class ScheduleRangeTooLong(AppException):
    status_code = 422
    detail = "Период расписания не может превышать 31 день."