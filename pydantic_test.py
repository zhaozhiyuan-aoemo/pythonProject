from pydantic import BaseModel, ValidationError, constr
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Column, Integer, String
import sqlalchemy.orm
from sqlalchemy.dialects.postgresql import ARRAY


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2023-11-07 12:22',
    'friends': [1, 2, '3']
}

user_data = {
    'id': 123,
    'name': 'Zed Z',
    'signup_ts': datetime(2023, 11, 7, 12, 22),
    'friends': [1, 2, 'asd']
}

user = User(**external_data)
print(user.id, user.signup_ts, user.friends)
print(user.model_dump())

try:
    User(id=111, signup_ts='2023-11-07 12:22', friends=[1, 2, 'not number'])
except ValidationError as e:
    print(e.json())

print(User.model_construct(**user_data))  # 不检验数据直接创建模型类，不推荐使用
print(User.model_fields.keys())  # 获取模型类的字段名


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound] = []


dog = Dog(birthday='2023-11-11', weight=10.5, sound=[Sound(sound='wang'), Sound(sound='wangwang')])  # 通过嵌套模型类创建模型类
print(dog.model_dump())

base = sqlalchemy.orm.declarative_base()


class CompanyOrm(base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        from_attributes = True


co_orm = CompanyOrm(id=1, public_key='123', name='123', domains=['123', '456'])
print(CompanyModel.model_validate(co_orm).model_dump())
