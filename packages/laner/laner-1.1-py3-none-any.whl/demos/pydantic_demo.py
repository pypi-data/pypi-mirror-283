# encoding: utf-8
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lane.chang on '07/07/2024'
    comment: 对pydantic扩展包使用的实例
"""
import json
from pydantic import Field  # 目前仅对pydantic的BaseModel进行了扩展，其他的沿用pydantic
from laner.pydantic import BaseModel


class Province(BaseModel):
    """ 省信息
    """
    code: str = Field('', title='省code')
    name: str = Field('', title='省名称')


class City(BaseModel):
    """ 市信息
    """
    code: str = Field('', title='市code')
    name: str = Field('', title='市名称')


class Address(BaseModel):
    """ 地址
    """
    province: Province = Field(None, title='省信息')
    city: City = Field(None, title='市信息')


class School(BaseModel):
    """ 学校信息
    """
    name: str = Field('', title='学校名')
    address: Address = Field('', title='学校地址信息')


class User(BaseModel):
    """ 用户信息
    """
    name: str = Field('', title='用户姓名')
    phone: str = Field('', title='用户手机号')
    school: School = Field(None, title='学校信息')


if __name__ == '__main__':

    user_info = {
        'name': 'lane',
        'phone': '13800000000',
        'school': {
            'name': '深圳师范学校',
            'address': {
                'province': {
                    'code': '440000',
                    'name': '广东省'
                },
                'city': {
                    'code': '0755',
                    'name': '深圳市'
                }
            }
        }
    }

    user = User()
    # 将信息匹配到自定义的模型中
    user.sets(user_info)
    # 展示模型信息
    print(json.dumps(user.dict(), ensure_ascii=False, indent=4))
