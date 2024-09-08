from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


class Fitness_center(Base):
    __tablename__ = 'fitness_center'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name_fc = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    contacts = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    birth_date = Column(String(50), default='1940-01-01', nullable=False)
    email = Column(String(50), nullable=False)
    funds = Column(Integer, default=0, nullable=False)

    def __init__(self, login, password, birth_date, email):
        self.login = login
        self.password = password
        self.birth_date = birth_date
        self.email = email
        self.funds = 0

    def add_funds(self, amount):
        if amount is not None and amount > 0:
            self.funds += amount

    def withdraw(self, amount):
        if amount is not None and amount > 0:
            new_funds = self.funds - amount
            self.funds = max(new_funds, 0)


# class Fitnes_center(Base):
#     __tablename__ = 'fitness_center'
#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     name_fc = Column(String(50), nullable=False)
#     address = Column(String(50), nullable=False)
#     contacts = Column(String(50), nullable=False)


class Treiner(Base):
    __tablename__ = 'trainer'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    fitness_center_id = Column(Integer, ForeignKey(Fitness_center.id))
    age = Column(Integer, nullable=False)
    sex = Column(String(50), nullable=False)


class Trainer_schedule(Base):
    __tablename__ = 'trainer_schedule'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    trainer_id = Column(Integer, ForeignKey(Treiner.id))
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)


class Review_rating(Base):
    __tablename__ = 'review_rating'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    point = Column(Integer, default=1, nullable=False)
    text = Column(String(50))
    trainer_id = Column(Integer, ForeignKey(Treiner.id))
    gym_id = Column(Integer, ForeignKey(Fitness_center.id))


class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    duration = Column(Integer, default=0, nullable=False)
    description = Column(String(50))
    price = Column(Integer, default=0, nullable=False)
    fitness_center_id = Column(Integer, ForeignKey(Fitness_center.id))
    max_atendees = Column(Integer, default=0, nullable=False)


class Trainer_service(Base):
    __tablename__ = 'trainer_service'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    max_attendees = Column(Integer, default=1, nullable=False)
    service_name = Column(String(50))
    trainer_name = Column(String(50))
    service_id = Column(Integer, ForeignKey(Service.id))
    trainer_id = Column(Integer, ForeignKey(Treiner.id))


class Balans(Base):
    __tablename__ = 'balans'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    service_id = Column(Integer, ForeignKey(Service.id))
    quantity_services = Column(Integer, nullable=False, default=0)


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    service_id = Column(Integer, ForeignKey(Service.id))
    trainer_id = Column(Integer, ForeignKey(Treiner.id))

    # def __repr__(self):
    #     return f'<User {self.name!r}>'