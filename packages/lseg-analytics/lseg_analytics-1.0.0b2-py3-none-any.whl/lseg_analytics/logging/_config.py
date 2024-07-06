import enum
import logging
import typing
from typing import List, Optional, Union

if typing.TYPE_CHECKING:
    from lseg_analytics.logging._logger import LibraryLogger


class LoggingOutput(enum.Enum):
    STDOUT = "stdout"
    FILE = "file"


class LoggingSection:
    def __init__(
        self,
        level: Optional[int] = None,
        outputs: Optional[List[LoggingOutput]] = None,
        *,
        default_section: "LoggingSection" = None,
    ):
        self._level = level
        # TODO: Improve Output configuration by adding file path, etc.
        if outputs is None:
            outputs = []
        self._outputs = outputs
        self._default_section = default_section
        self._loggers: List["LibraryLogger"] = []

    @property
    def level(self):
        if self._level is None:
            return self._default_section.level
        return self._level

    @level.setter
    def level(self, value: Union[int, None]):
        if self._default_section is None and value is None:
            raise ValueError("Cannot set level to None for default section")
        self._level = value
        for logger in self._loggers:
            logger.update_level_from_config()

    @property
    def outputs(self):
        default_output = self._default_section.outputs if self._default_section else []
        return self._outputs + default_output

    def add_output(self, output: LoggingOutput):
        self._outputs.append(output)
        for logger in self._loggers:
            logger.update_config()

    def remove_output(self, output: LoggingOutput):
        self._outputs.remove(output)
        for logger in self._loggers:
            logger.update_config()

    def add_logger(self, logger: "LibraryLogger"):
        self._loggers.append(logger)


class LoggingConfiguration:
    def __init__(self):
        self._modules = {
            "DEFAULT": LoggingSection(
                level=logging.INFO,
                outputs=[LoggingOutput.STDOUT],
            )
        }

    def __getitem__(self, module_name):
        module_name = module_name.upper()
        if module_name not in self._modules:
            self._modules[module_name] = LoggingSection(default_section=self["DEFAULT"])
        return self._modules[module_name]


library_config = LoggingConfiguration()
