from django.db.utils import IntegrityError


class ParentDoesNotExist(IntegrityError):
    pass
