import datetime

# from flask import Flask, request, render_template, session, redirect
# from SqlLIteDB_test import Dbsql, login_required

from flask import Flask, request, render_template, session, redirect
from sqlalchemy import select

from SqlLIteDB_test import Dbsql, login_required
import database, models
from sqlalchemy.orm import joinedload



app = Flask(__name__)
app.secret_key = "mzdfhgvbdatJT67tdcghb"

def check_existence(username, password):
    table = 'user'
    colons = None
    condition = {'login': username, 'password': password}
    with Dbsql('db') as db:
        user = db.fetch_one(table, colons, condition)
    return user is not None



def clac_slots(trainer_id, service_id, formatted_date):
    database.init_db()
    #
    booket_time = (
    database.db_session.query(models.Reservation.date, models.Reservation.time, models.Service.duration)
    .join(models.Service, models.Reservation.service_id == models.Service.id)
    .filter(models.Reservation.trainer_id == trainer_id, models.Reservation.date == formatted_date)
    .all()
    )

    # booket_time = database.db_session.query(models.Reservation).join(models.Service, models.Reservation.service_id==models.Service.id).filter(trainer_id=trainer_id, date=formatted_date).all()
    trainer_schedule = database.db_session.query(models.Trainer_schedule).filter_by(trainer_id=trainer_id, date=formatted_date).one()
    trainer_capacity = database.db_session.query(models.Trainer_service).filter_by(trainer_id=trainer_id, service_id=service_id).one()
    service_info = database.db_session.query(models.Service).filter_by(id=service_id).one()
    print(trainer_schedule)
    print(booket_time)
    print(trainer_capacity)
    print(service_info)


    # with Dbsql('db') as db:
    #
    #     table = 'reservation'
    #     colons = None
    #     condition = {'trainer_id': trainer_id, 'date' : formatted_date}
    #     join_condition = {'service.id': 'reservation.service_id'}
    #     booket_time = db.fetch_oll(table, colons, condition, join_table='service', join_condition=join_condition)
    #
    #     table = 'trainer_schedule'
    #     colons = None
    #     condition = {'trainer_id': trainer_id, 'date' : formatted_date}
    #     trainer_schedule = db.fetch_one(table, colons, condition)
    #
    #     table = 'trainer_service'
    #     colons = None
    #     condition = {'trainer_id': trainer_id, 'service_id': service_id}
    #     trainer_capacity = db.fetch_one(table, colons, condition)
    #
    #     table = 'service'
    #     colons = None
    #     condition = {'id': service_id}
    #     service_info = db.fetch_one(table, colons, condition)


    start_dt = datetime.datetime.strptime(trainer_schedule.date + ' ' + trainer_schedule.start_time, '%d.%m.%Y %H:%M')
    end_dt = datetime.datetime.strptime(trainer_schedule.date + ' ' + trainer_schedule.end_time, '%d.%m.%Y %H:%M')
    cur_dt = start_dt
    trainer_schedule = {}

    while cur_dt < end_dt:
        trainer_schedule[cur_dt] = trainer_capacity.max_attendees
        cur_dt = cur_dt + datetime.timedelta(minutes=15)

    if booket_time is not None:

        for one_booking in booket_time:
            booking_date = one_booking[0]
            booking_time = one_booking[1]
            booking_duration = one_booking[2]
            one_booking_start = datetime.datetime.strptime(booking_date + " " + booking_time,  '%d.%m.%Y %H:%M')
            booking_end = one_booking_start + datetime.timedelta(minutes=booking_duration)
            cur_dt = one_booking_start
            while cur_dt < booking_end:
                trainer_schedule[cur_dt] -= 1
                cur_dt += datetime.timedelta(minutes=15)
    else:
       print(trainer_schedule, cur_dt)

    result_time = []
    srvice_duration = service_info.duration
    srvice_start_time = start_dt
    while srvice_start_time < end_dt:
        service_end_time = srvice_start_time + datetime.timedelta(minutes=srvice_duration)
        everyting_is_free = True
        iter_start_time = srvice_start_time
        while iter_start_time < service_end_time:
            if trainer_schedule[iter_start_time] == 0 or service_end_time > end_dt:
                everyting_is_free = False
                break

            iter_start_time +=datetime.timedelta(minutes=15)


        if everyting_is_free:
            result_time.append(srvice_start_time)

        srvice_start_time += datetime.timedelta(minutes=15)
    final_result = [datetime.datetime.strftime(el, '%H:%M') for el in result_time]

    print(trainer_schedule)
    print(booket_time)
    print(trainer_schedule)
    print(result_time)
    print(final_result)
    return final_result

    # time_duration = datetime.datetime(year=2024, month=5, day=31, minute=0 ) + datetime.timedelta(minutes=15)

    # clac_slots(1,1, '31.05.2024')
