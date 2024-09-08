import os

from flask import Flask, request, render_template, session, redirect

from send_email import send_email
from SqlLIteDB_test import login_required
import database, models
# from utils_test import clac_slots
from utils import clac_slots

from datetime import datetime


import sqlite3
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)
app.secret_key = os.getenv('APP_PASSWORD')



def check_existence(username, password):
    database.init_db()
    user = database.db_session.query(models.User).filter_by(login = username, password = password).first()

    return user


@app.get('/')
def home():

    return render_template('home.html')


@app.post('/register')
def new_user_register():
    from_data = request.form

    database.init_db()
    user1 = models.User( login = from_data['login'],
                         password = from_data['password'],
                         birth_date = from_data['birth_date'],
                         phone = from_data['phone'],
                         email = from_data['email'])
    database.db_session.add(user1)
    database.db_session.commit()

    return render_template('register_add.html', login=from_data['login'])


@app.get('/register')
def user_register_invitation():
    return render_template("register.html")





@app.post('/login')
def user_login():
    from_data = request.form
    login = request.form['login']
    password = request.form['password']
    user = check_existence(login, password)
    if user is not None:

        session['user_id'] = {"id" : user.id, 'login': user.login}
        return redirect('/user')
    else:
        return redirect('/bad_login_or_password')


@app.get('/login')
def user_login_form():
    user = session.get('user_id', None)
    if user:
        return redirect('/user')
    else:
        return render_template('login.html')


@app.get('/bad_login_or_password')
def bad_login():
    return render_template('bad_login_or_password.html')


@app.get('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.post('/user')
def add_user_info():
    return 'user data were modified'


@app.get('/user')
@login_required

def user_info():

    user_id = session.get('user_id', None)

    user_id_c = user_id['id']
    database.init_db()
    res = database.db_session.query(models.User).filter_by(id = user_id_c).all()

    return render_template("user.html", res = res)



@app.put('/user')
def user_update():
    return 'user info was successfully updated'


@app.post('/funds')
def add_funds():
    return 'user accound was successfully funds'


@app.get('/funds')
@login_required

def user_deposit_info():
    user_id = session.get('user_id', None)
    database.init_db()
    res = database.db_session.query(models.User).filter_by(id=user_id).one()



    return render_template("funds.html", res = res.funds)


@app.post('/reservations')
def add_reservations():
    user_id = session.get('user_id', None)
    user_id_c = user_id['id']
    from_data = request.form
    database.init_db()
    trainar_name = database.db_session.query(models.Treiner).filter_by(id=int(from_data['trainer_id'])).one()
    service_name = database.db_session.query(models.Service).filter_by(id=int(from_data['service_id'])).one()
    user_email = database.db_session.query(models.User).filter_by(id=user_id_c).one()

    res = models.Reservation(user_id=user_id_c, date=from_data['date'], time=from_data['slots'], trainer_id=int(from_data['trainer_id']), service_id=int(from_data['service_id']))
    database.db_session.add(res)
    database.db_session.commit()

    send_email.delay(from_data['date'], from_data['slots'], trainar_name.name, service_name.name, user_email.email)
    return render_template('home.html')





@app.get('/reservations')
@login_required

def user_reservations_list_info():
    user_id = session.get('user_id', None)
    user_id_c = user_id['id']

    database.init_db()
    res = database.db_session.query(models.Reservation.id, models.Reservation.date, models.Reservation.time).filter_by(user_id=user_id_c).all()

    return render_template("reservations.html", res = res)

@app.post('/delete_reservation/<reservation_id>')

def delete_reservation(reservation_id):
    user_id = session.get('user_id', None)
    user_id_c = user_id['id']

    from_data = request.form
    service_id = from_data.get('service_id')

    database.init_db()
    res = database.db_session.query(models.Reservation).filter_by(user_id=user_id_c, id=from_data['id'] ).first()
    database.db_session.delete(res)
    database.db_session.commit()
    return redirect('/')


@app.get('/reservations/<reservation_id>')
@login_required

def user_reservations_info(reservation_id):
    user_id = session.get('user_id', None)
    database.init_db()
    res = (
        database.db_session.query(
            models.Reservation.date,
            models.Reservation.time,
            models.Service.price,
            models.Service.name
        )
        .join(models.Service, models.Reservation.service_id == models.Service.id)
        .filter(models.Reservation.id == reservation_id, models.Reservation.user_id == user_id['id'])
        .all()
    )


    return render_template("reservation_id.html", reservation_id=reservation_id, res = res)




@app.delete('/reservations/<reservation_id>')
def delete_reservations(reservation_id):
    return f'user reservations {reservation_id} was successfully deleted'


@app.post('/checkout')
def add_checkout_order_service():
    return 'add checkout order service'


@app.get('/checkout')
def checkout_info():
    database.init_db()
    res = database.db_session.query(models.Service.name, models.Service.price).all()

    return render_template("checkout.html", res = res)


@app.put('/checkout')
def update_checkout_order_service():
    return 'checkout order service was successfully updated'


@app.get('/fitness_center')
def get_fitness_center():
    database.init_db()
    res = database.db_session.query(models.Fitness_center.name_fc, models.Fitness_center.address, models.Fitness_center.id,).all()


    return render_template("fitness_center.html", res = res)

@app.get('/fitness_center/<gym_id>')
def get_fitness_center_info(gym_id):
    database.init_db()
    res = (
        database.db_session.query(
            models.Fitness_center.id,
            models.Treiner.fitness_center_id,
            models.Treiner.id,
            models.Treiner.name,
            models.Treiner.sex

        )
        .join(models.Treiner, models.Treiner.fitness_center_id == models.Fitness_center.id)
        .filter(models.Fitness_center.id == gym_id)
        .all()
    )



    res_s = (
        database.db_session.query(
            models.Fitness_center.id,
            models.Service.fitness_center_id,
            models.Service.id,
            models.Service.name,
            models.Service.price

        )
        .join(models.Service, models.Service.fitness_center_id == models.Fitness_center.id)
        .filter(models.Fitness_center.id == gym_id)
        .all()
    )

    return render_template("gym_id.html", res = res, res_s = res_s, gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/service')
def get_service(gym_id):
    database.init_db()

    res = database.db_session.query(models.Service.name).filter_by(fitness_center_id=gym_id).all()



    return render_template("service.html", res = res, gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/service/<service_id>')
def get_service_info(gym_id, service_id):
    database.init_db()

    res_s = (
        database.db_session.query(
            models.Service.id,
            models.Service.name,
            models.Service.duration,
            models.Service.description,
            models.Service.price,
            models.Service.fitness_center_id,
            models.Service.max_atendees,
            models.Trainer_service.trainer_id,
            models.Trainer_service.service_id,
            models.Trainer_service.max_attendees,
            models.Trainer_service.service_name,
            models.Trainer_service.trainer_name,

    )
        .join(models.Trainer_service, models.Trainer_service.service_id == service_id)
        .filter(models.Service.id == service_id, models.Service.fitness_center_id==gym_id)
        .all()
    )

    keys =['id','name','duration','description','price','fitness_center_id','max_atendees','trainer_id','service_id','max_attendees','service_name','trainer_name']
    v= res_s
    res1 =[dict(zip(keys, values)) for values in v]


    return render_template("service_id.html", res = res1, service_id=service_id, gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/trainer')
def get_trainer(gym_id):
    database.init_db()
    res = database.db_session.query(models.Treiner.name).filter_by(fitness_center_id=gym_id).all()




    return render_template("trainer.html", res = res,  gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/trainer/<trainer_id>')
def get_coach_info(gym_id, trainer_id):
    database.init_db()

    res_s = (
        database.db_session.query(
            models.Treiner.id,
            models.Treiner.name,
            models.Treiner.fitness_center_id,
            models.Treiner.age,
            models.Treiner.sex,
            models.Trainer_service.trainer_id,
            models.Trainer_service.service_id,
            models.Trainer_service.max_attendees,
            models.Trainer_service.service_name,
            models.Trainer_service.trainer_name,

        )
        .join(models.Trainer_service, models.Trainer_service.trainer_id == trainer_id)
        .filter(models.Treiner.id == trainer_id, models.Treiner.fitness_center_id == gym_id)
        .all()
    )

    keys = ['id', 'name', 'fitness_center_id', 'age', 'sex', 'trainer_id',
            'service_id', 'max_attendees', 'service_name', 'trainer_name']
    v = res_s
    res1 = [dict(zip(keys, values)) for values in v]
    rating = database.db_session.query(models.Review_rating).filter_by(trainer_id=trainer_id).all()



    return render_template("trainer_id.html", res = res1, trainer_id=trainer_id, gym_id=gym_id, rating=rating)


@app.get('/fitness_center/<gym_id>/trainer/<trainer_id>/score')
@login_required

def get_coach_score(gym_id, trainer_id):
    return render_template('score.html', gym_id=gym_id, trainer_id=trainer_id)



@login_required
@app.post('/fitness_center/<gym_id>/trainer/<trainer_id>/score')
def set_coach_score(gym_id, trainer_id):
    user_id = session.get('user_id', None)

    from_data = request.form

    database.init_db()
    res = database.db_session.query(models.Review_rating).filter_by(gym_id=from_data['gym_id'], trainer_id=from_data['trainer_id'], user_id=user_id['id']).first()
    if res is not None:
        res.point = from_data['point']
        res.text = from_data['text']
        database.db_session.commit()

        return render_template('score_add.html', gym_id=from_data['gym_id'], trainer_id=from_data['trainer_id'])

    else:

        rese = models.Review_rating(user_id=user_id['id'], point=int(from_data['point']), text=str(from_data['text']),  trainer_id=from_data['trainer_id'], gym_id=from_data['gym_id'])


        database.db_session.add(rese)
        database.db_session.commit()
        return render_template('score_add.html', gym_id=from_data['gym_id'], trainer_id=from_data['trainer_id'])




@app.put('/fitness_center/<gym_id>/trainer/<trainer_id>/score')
def update_coach_score(gym_id, trainer_id):
    return f'fitness center {gym_id} trainer {trainer_id} score was updated'


@app.get('/fitness_center/<gym_id>/loyality_programs')
def get_loyality_programs(gym_id):
    database.init_db()
    res = database.db_session.query(models.Fitness_center.name_fc).filter_by(id=gym_id).all()


    return render_template('loyality_programs.html', res=res)


@app.post('/pre_reservation')
@login_required

def pre_reservation():
    user_id = session.get('user_id', None)
    from_data = request.form
    trainer = from_data['trainer_id']
    service = from_data['service_id']
    desired_date = from_data['desired_date']
    original_date = desired_date
    parsed_date = datetime.strptime(original_date, "%Y-%m-%d")
    formatted_date = parsed_date.strftime("%d.%m.%Y")

    time_slots = clac_slots(trainer, service, formatted_date)

    return render_template('pre_reservation.html', form_info={'trainer_id':trainer, 'service_id':service, 'time_slots':time_slots, 'formatted_date': formatted_date})



if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8080
    app.run(host=host, port=port, debug=False)
