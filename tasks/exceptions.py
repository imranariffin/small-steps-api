from django.db.utils import IntegrityError


class ParentDoesNotExist(IntegrityError):
    pass

class StatusTransitionError(Exception):
    pass
