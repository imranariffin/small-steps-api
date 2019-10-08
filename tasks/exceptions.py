from django.db.utils import IntegrityError


class ParentDoesNotExist(IntegrityError):
    pass


class InvalidStatusTransition(Exception):
    pass
