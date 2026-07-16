from pydantic import BaseModel, field_validator

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    number_of_class: int
    phone: str | None = None
    parent_name: str | None = None
    parent_phone: str | None = None
    notes: str | None = None
    is_active: bool = True

    @field_validator("first_name", "parent_name")
    @classmethod
    def validate_name(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Имя не может быть пустым")

        if len(value) > 100:
            raise ValueError("Длина имени должна быть не более 100 символов")

        return value
        
    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Фамилия не может быть пустой")
        
        if len(value) > 100:
            raise ValueError("Длина фамилии должна быть не более 100 символов")

        return value

    @field_validator("number_of_class")
    @classmethod
    def validate_number_of_class(cls, value):
        if not 1 <= value <= 11:
            raise ValueError(
                "Номер класса должен быть от 1 до 11 включительно"
            )
        return value
        
    @field_validator("phone", "parent_phone")
    @classmethod
    def validate_phone(cls, value: str | None):
        if value is None:
            return value
        
        value = value.strip()
        
        if value.startswith("+7"):
            digits = value[1:]
        elif value.startswith("8"):
            digits = value
        else:
            raise ValueError("Телефон должен начинаться с +7 или 8")

        if not digits.isdigit():
            raise ValueError("Телефон должен содержать только цифры")

        if len(digits) != 11:
            raise ValueError("Телефон должен содержать 11 цифр")

        return value
    
    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: str | None):
        if value is None:
            return value
        
        if len(value) > 1000:
            raise ValueError("Комментарий слишком длинный (больше 1000 символов)")
        
        return value

    

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    number_of_class: int
    phone: str | None = None
    parent_name: str | None = None
    parent_phone: str | None = None
    notes: str | None = None
    is_active: bool

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    number_of_class: int | None = None
    phone: str | None = None
    parent_name: str | None = None
    parent_phone: str | None = None
    notes: str | None = None
    is_active: bool | None = None

    @field_validator("first_name", "parent_name")
    @classmethod
    def validate_name(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Имя не может быть пустым")

        if len(value) > 100:
            raise ValueError("Длина имени должна быть не более 100 символов")

        return value
        
    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value):
        if value is None:
            return value
        
        value = value.strip()

        if not value:
            raise ValueError("Фамилия не может быть пустой")
        
        if len(value) > 100:
            raise ValueError("Длина фамилии должна быть не более 100 символов")

        return value

    @field_validator("number_of_class")
    @classmethod
    def validate_number_of_class(cls, value):
        if value is None:
            return value

        if not 1 <= value <= 11:
            raise ValueError(
                "Номер класса должен быть от 1 до 11 включительно"
            )
        return value
        
    @field_validator("phone", "parent_phone")
    @classmethod
    def validate_phone(cls, value: str | None):
        if value is None:
            return value
        
        value = value.strip()
        
        if value.startswith("+7"):
            digits = value[1:]
        elif value.startswith("8"):
            digits = value
        else:
            raise ValueError("Телефон должен начинаться с +7 или 8")

        if not digits.isdigit():
            raise ValueError("Телефон должен содержать только цифры")

        if len(digits) != 11:
            raise ValueError("Телефон должен содержать 11 цифр")

        return value
    
    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: str | None):
        if value is None:
            return value
        
        if len(value) > 1000:
            raise ValueError("Комментарий слишком длинный (больше 1000 символов)")
        
        return value