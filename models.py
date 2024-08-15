from sqlalchemy import Column, Integer, String, DateTime
from database import Base


# class Fitness_center(Base):
#     __tablename__ = 'fitness_center'
#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     name_fc = Column(String(50),  nullable=False)
#     address = Column(String(50), nullable=False)
#     contacts = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    birth_date = Column(String(50), default='1940-01-01', nullable=False)
    phone = Column(String(50), nullable=False)
    funds = Column(Integer, default=0, nullable=False)

    def __init__(self, login, password, birth_date, phone):
        self.login = login
        self.password = password
        self.birth_date = birth_date
        self.phone = phone
        self.funds = 0

    def add_funds(self, amount):
        if amount is not None and amount > 0:
            self.funds += amount


    def withdraw(self, amount):
        if amount is not None and amount > 0:
            new_funds = self.funds - amount
            self.funds = max(new_funds, 0)


    # def __repr__(self):
    #     return f'<User {self.name!r}>'