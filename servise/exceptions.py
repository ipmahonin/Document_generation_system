class NotFoundError(Exception):
    """Объект не найден -> HTTP 404"""
    pass

class ConflictError(Exception):
    """Конфликт (например, дубликат) -> HTTP 409"""
    pass

class UnauthorizedError(Exception):
    """Ошибка аутентификации -> HTTP 401"""
    pass

class BadRequestError(Exception):
    """Некорректные данные или нарушение бизнес-правил -> HTTP 400"""
    pass

