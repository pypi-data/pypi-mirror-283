# encoding: utf-8
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lane.chang on '07/07/2024'
    comment: 对pydantic包进行扩展
"""
import types
from typing import Union
from enum import Enum

from pydantic import BaseModel as PydBase


class BaseModel(PydBase):
    """ pydantic BaseModel的扩展
    """

    @classmethod
    def get_model_field(cls, name):
        """
        :param name:
        :return:
        """
        for k, v in cls.__fields__.items():
            if k != name:
                continue
            return v

    def sets(self, elements: Union[dict, PydBase]):
        """ 批量设置对象元素(dict)
        :param elements:
        :return:
        """
        if isinstance(elements, PydBase):
            elements = elements.dict()

        for k, v in elements.items():
            if not hasattr(self, k):
                continue

            model_field = self.__class__.get_model_field(k)
            if not model_field:
                continue

            # 泛型
            if issubclass(type(model_field.outer_type_), types.GenericAlias):
                _instances = []
                _class = None
                if model_field.outer_type_.__origin__ is list:
                    for sub_field in model_field.sub_fields:
                        if callable(model_field.type_):
                            continue
                        if not issubclass(sub_field.type_, BaseModel):
                            continue
                        _class = sub_field.type_

                    if not _class:
                        continue
                    for _v in v:
                        _instance = _class()
                        _instance.sets(_v)
                        _instances.append(_instance)

                    setattr(self, k, _instances)
                elif model_field.outer_type_.__origin__ is dict:
                    for sub_field in model_field.sub_fields:
                        if not issubclass(sub_field.type_, BaseModel):
                            continue
                        _class = sub_field.type_

                    if not _class:
                        continue

                    _instance = _class()
                    _instance.sets(v)

                    setattr(self, k, _instance)
                else:
                    setattr(self, k, v)
            #  callable(_model_field.type_) 是为了过滤typing.Union的场景
            elif not callable(model_field.type_) and issubclass(model_field.type_, BaseModel):
                _instance = model_field.type_()
                _instance.sets(v)
                setattr(self, k, _instance)
            else:
                setattr(self, k, v)

    def dict(self, *args, **kwargs) -> dict:
        """ 扩展dict功能
        :param args:
        :param kwargs:
        :return:
        """
        result = super(BaseModel, self).dict(*args, **kwargs)

        def _convert_enum(value: Union[list, dict]):
            """
            :param value:
            :return:
            """
            if isinstance(value, list):
                for idx, v in enumerate(value):
                    if isinstance(v, Enum):
                        value[idx] = v.value
                    elif isinstance(v, (list, dict)):
                        _convert_enum(v)

            elif isinstance(value, dict):
                for k, v in value.items():
                    # 支持枚举类型
                    if isinstance(v, Enum):
                        v = v.value
                    elif isinstance(v, (list, dict)):
                        _convert_enum(v)

                    value[k] = v

        _convert_enum(result)

        return result
