from logging import getLogger
from typing import Any


class Logger:
    def __init__(self, name: str) -> None:
        self.log = getLogger(name)
        self.name = name

    @staticmethod
    def format_message(message: str, tag: str) -> str:
        sub_tag = f"[{tag}]" if tag else ""
        return f"{sub_tag} {message}"

    @staticmethod
    def __get_base_handler_config() -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "verbose": {
                    "class": "logging.Formatter",
                    "format": "%(asctime)s %(levelname)-7.7s: [%(name)-15.15s][%(threadName)-15.15s]  %(message)s",
                }
            },
        }

    @staticmethod
    def get_stdout_handler_config(stdout_level: str) -> dict[str, Any]:
        return {
            **Logger.__get_base_handler_config(),
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "level": f"{stdout_level}",
                    "formatter": "verbose",
                },
            },
            "root": {
                "handlers": ["stdout"],
                "level": "DEBUG",
            },
        }

    def d(
        self,
        message: str,
        tag: str,
        exc_info: bool | Exception = False,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: dict[str, str] | None = None,
    ) -> None:
        """
        You can specify stack_info independently of exc_info, e.g. to just show how you got to a certain point in your
        code, even when no exceptions were raised. The stack frames are printed following a header line which says:

        > Stack (most recent call last):

        :param message: Log message
        :param tag: function name for better filtering
        :param exc_info: If exc_info does not evaluate as false, it causes exception information to be added to the
        logging message. If an exception tuple (in the format returned by sys.exc_info()) or an exception instance is
        provided, it is used; otherwise, sys.exc_info() is called to get the exception information.
        :param stack_info: If true, stack information is added to the logging message, including the actual logging
        call. Note that this is not the same stack information as that displayed through specifying exc_info: The former
        is stack frames from the bottom of the stack up to the logging call in the current thread, whereas the latter is
        information about stack frames which have been unwound, following an exception, while searching for exception
        handlers.
        :param stacklevel: If greater than 1, the corresponding number of stack frames are skipped when computing the
        line number and function name set in the LogRecord created for the logging event. This can be used in logging
        helpers so that the function name, filename and line number recorded are not the information for the helper
        function/method, but rather its caller. The name of this parameter mirrors the equivalent one in the warnings
        module.
        :param extra: Can be used to pass a dictionary which is used to populate the __dict__ of the LogRecord created
        for the logging event with user-defined attributes. These custom attributes can then be used as you like. For
        example, they could be incorporated into logged messages.
        """
        self.log.debug(
            Logger.format_message(message, tag),
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def i(
        self,
        message: str,
        tag: str,
        exc_info: bool | Exception = False,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: dict[str, str] | None = None,
    ) -> None:
        """
        You can specify stack_info independently of exc_info, e.g. to just show how you got to a certain point in your
        code, even when no exceptions were raised. The stack frames are printed following a header line which says:

        > Stack (most recent call last):

        :param message: Log message
        :param tag: function name for better filtering
        :param exc_info: If exc_info does not evaluate as false, it causes exception information to be added to the
        logging message. If an exception tuple (in the format returned by sys.exc_info()) or an exception instance is
        provided, it is used; otherwise, sys.exc_info() is called to get the exception information.
        :param stack_info: If true, stack information is added to the logging message, including the actual logging
        call. Note that this is not the same stack information as that displayed through specifying exc_info: The former
        is stack frames from the bottom of the stack up to the logging call in the current thread, whereas the latter is
        information about stack frames which have been unwound, following an exception, while searching for exception
        handlers.
        :param stacklevel: If greater than 1, the corresponding number of stack frames are skipped when computing the
        line number and function name set in the LogRecord created for the logging event. This can be used in logging
        helpers so that the function name, filename and line number recorded are not the information for the helper
        function/method, but rather its caller. The name of this parameter mirrors the equivalent one in the warnings
        module.
        :param extra: Can be used to pass a dictionary which is used to populate the __dict__ of the LogRecord created
        for the logging event with user-defined attributes. These custom attributes can then be used as you like. For
        example, they could be incorporated into logged messages.
        """
        self.log.info(
            Logger.format_message(message, tag),
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def w(
        self,
        message: str,
        tag: str,
        exc_info: bool | Exception = False,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: dict[str, str] | None = None,
    ) -> None:
        """
        You can specify stack_info independently of exc_info, e.g. to just show how you got to a certain point in your
        code, even when no exceptions were raised. The stack frames are printed following a header line which says:

        > Stack (most recent call last):

        :param message: Log message
        :param tag: function name for better filtering
        :param exc_info: If exc_info does not evaluate as false, it causes exception information to be added to the
        logging message. If an exception tuple (in the format returned by sys.exc_info()) or an exception instance is
        provided, it is used; otherwise, sys.exc_info() is called to get the exception information.
        :param stack_info: If true, stack information is added to the logging message, including the actual logging
        call. Note that this is not the same stack information as that displayed through specifying exc_info: The former
        is stack frames from the bottom of the stack up to the logging call in the current thread, whereas the latter is
        information about stack frames which have been unwound, following an exception, while searching for exception
        handlers.
        :param stacklevel: If greater than 1, the corresponding number of stack frames are skipped when computing the
        line number and function name set in the LogRecord created for the logging event. This can be used in logging
        helpers so that the function name, filename and line number recorded are not the information for the helper
        function/method, but rather its caller. The name of this parameter mirrors the equivalent one in the warnings
        module.
        :param extra: Can be used to pass a dictionary which is used to populate the __dict__ of the LogRecord created
        for the logging event with user-defined attributes. These custom attributes can then be used as you like. For
        example, they could be incorporated into logged messages.
        """
        self.log.warning(
            Logger.format_message(message, tag),
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def e(
        self,
        message: str,
        tag: str,
        exc_info: bool | Exception = False,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: dict[str, str] | None = None,
    ) -> None:
        """
        You can specify stack_info independently of exc_info, e.g. to just show how you got to a certain point in your
        code, even when no exceptions were raised. The stack frames are printed following a header line which says:

        > Stack (most recent call last):

        :param message: Log message
        :param tag: function name for better filtering
        :param exc_info: If exc_info does not evaluate as false, it causes exception information to be added to the
        logging message. If an exception tuple (in the format returned by sys.exc_info()) or an exception instance is
        provided, it is used; otherwise, sys.exc_info() is called to get the exception information.
        :param stack_info: If true, stack information is added to the logging message, including the actual logging
        call. Note that this is not the same stack information as that displayed through specifying exc_info: The former
        is stack frames from the bottom of the stack up to the logging call in the current thread, whereas the latter is
        information about stack frames which have been unwound, following an exception, while searching for exception
        handlers.
        :param stacklevel: If greater than 1, the corresponding number of stack frames are skipped when computing the
        line number and function name set in the LogRecord created for the logging event. This can be used in logging
        helpers so that the function name, filename and line number recorded are not the information for the helper
        function/method, but rather its caller. The name of this parameter mirrors the equivalent one in the warnings
        module.
        :param extra: Can be used to pass a dictionary which is used to populate the __dict__ of the LogRecord created
        for the logging event with user-defined attributes. These custom attributes can then be used as you like. For
        example, they could be incorporated into logged messages.
        """
        self.log.error(
            Logger.format_message(message, tag),
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def c(
        self,
        message: str,
        tag: str,
        exc_info: bool | Exception = False,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: dict[str, str] | None = None,
    ) -> None:
        """
        You can specify stack_info independently of exc_info, e.g. to just show how you got to a certain point in your
        code, even when no exceptions were raised. The stack frames are printed following a header line which says:

        > Stack (most recent call last):

        :param message: Log message
        :param tag: function name for better filtering
        :param exc_info: If exc_info does not evaluate as false, it causes exception information to be added to the
        logging message. If an exception tuple (in the format returned by sys.exc_info()) or an exception instance is
        provided, it is used; otherwise, sys.exc_info() is called to get the exception information.
        :param stack_info: If true, stack information is added to the logging message, including the actual logging
        call. Note that this is not the same stack information as that displayed through specifying exc_info: The former
        is stack frames from the bottom of the stack up to the logging call in the current thread, whereas the latter is
        information about stack frames which have been unwound, following an exception, while searching for exception
        handlers.
        :param stacklevel: If greater than 1, the corresponding number of stack frames are skipped when computing the
        line number and function name set in the LogRecord created for the logging event. This can be used in logging
        helpers so that the function name, filename and line number recorded are not the information for the helper
        function/method, but rather its caller. The name of this parameter mirrors the equivalent one in the warnings
        module.
        :param extra: Can be used to pass a dictionary which is used to populate the __dict__ of the LogRecord created
        for the logging event with user-defined attributes. These custom attributes can then be used as you like. For
        example, they could be incorporated into logged messages.
        """
        self.log.critical(
            Logger.format_message(message, tag),
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def exception(
        self,
        message: str,
        tag: str,
        exc_info: bool | Exception = True,
        stack_info: bool = True,
        stacklevel: int = 1,
        extra: dict[str, str] | None = None,
    ) -> None:
        """
        Exception info is added to the logging message. This method should only be called from an exception handler.

        You can specify stack_info independently of exc_info, e.g. to just show how you got to a certain point in your
        code, even when no exceptions were raised. The stack frames are printed following a header line which says:

        > Stack (most recent call last):

        :param message: Log message
        :param tag: function name for better filtering
        :param exc_info: If exc_info does not evaluate as false, it causes exception information to be added to the
        logging message. If an exception tuple (in the format returned by sys.exc_info()) or an exception instance is
        provided, it is used; otherwise, sys.exc_info() is called to get the exception information.
        :param stack_info: If true, stack information is added to the logging message, including the actual logging
        call. Note that this is not the same stack information as that displayed through specifying exc_info: The former
        is stack frames from the bottom of the stack up to the logging call in the current thread, whereas the latter is
        information about stack frames which have been unwound, following an exception, while searching for exception
        handlers.
        :param stacklevel: If greater than 1, the corresponding number of stack frames are skipped when computing the
        line number and function name set in the LogRecord created for the logging event. This can be used in logging
        helpers so that the function name, filename and line number recorded are not the information for the helper
        function/method, but rather its caller. The name of this parameter mirrors the equivalent one in the warnings
        module.
        :param extra: Can be used to pass a dictionary which is used to populate the __dict__ of the LogRecord created
        for the logging event with user-defined attributes. These custom attributes can then be used as you like. For
        example, they could be incorporated into logged messages.
        """
        self.log.exception(
            Logger.format_message(message, tag),
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )