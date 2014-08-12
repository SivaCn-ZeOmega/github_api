

class BaseException(Exception):
    pass


class ArgumentError(BaseException):
    pass


class EmptyRequestBodyError(BaseException):
    pass


class NotValidRequest(BaseException):
    pass


class HookError(Exception):
    pass

class NotHookedForPullRequest(HookError):
    pass
