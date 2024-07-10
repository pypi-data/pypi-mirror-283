from __future__ import annotations

from typing import Self, Union

from .i18n import tr


class Error:
    _type_classes: dict[str, type[Error]] = dict()

    app: str = ''
    type: str
    msg: str = ''
    tr_key: str = ''

    @property
    def message(self):
        if self.tr_key:
            return tr('.'.join([self.app, self.tr_key]))
        return tr('.'.join([self.app, self.type]), default=self.msg)

    def __repr__(self):
        return f'Error [{self.app}] ({self.type}): \"{self.message}\"'

    def __eq__(self, other: Self):
        return (self.app, self.type) == (other.app, other.type)

    def __hash__(self):
        return hash((self.app, self.type))

    @property
    def dict(self):
        return dict(app=self.app, type=self.type, message=self.message)

    @classmethod
    def get_by_type(cls, type_: str) -> Union[type[Self], None]:
        return cls._type_classes.get(type_)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'type'):
            cls._type_classes[cls.type] = cls


class ErrorKwargsMixin:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    # noinspection PyUnresolvedReferences
    @property
    def message(self):
        message = super(ErrorKwargsMixin, self).message
        return message.format(**self.kwargs)
