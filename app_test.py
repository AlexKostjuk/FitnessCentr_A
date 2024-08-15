from flask import Flask, request, render_template, session, redirect
from SqlLIteDB_test import Dbsql, login_required
import database, models
from utils_test import clac_slots
from datetime import datetime


import sqlite3



app = Flask(__name__)
app.secret_key = "mzdfhgvbdatJT67tdcghb"



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
                         phone = from_data['phone'])
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
    print(user)
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
    user_id_c = user_id['id']
    database.init_db()
    res = database.db_session.query(models.User).filter_by(id=user_id_c).one()
    print(res)


    # table = 'user'
    # colons = 'funds'
    # condition = {'id': user_id}
    # with Dbsql('db') as db:
    #     res = db.fetch_oll(table, colons, condition)
    # # return res

    return render_template("funds.html", res = res.funds)


@app.post('/reservations')
def add_reservations():
    user_id = session.get('user_id', None)
    from_data = request.form
    table_bd = "reservation"
    k_r = {'user_id': user_id, 'date': from_data['date'], 'time': from_data['slots'],
           'trainer_id': from_data['trainer_id'], 'service_id': from_data['service_id']}
    with Dbsql('db') as db:

        db.insert_to_db(table_bd, k_r)
    return render_template('home.html')

    # from_dict = request.form
    # servise_id = from_dict['service_id']
    # trainer_id = from_dict['trainer_id']


    return ' new reservations was successfully'


@app.get('/reservations')
@login_required

def user_reservations_list_info():
    user_id = session.get('user_id', None)

    # a = 'select service_id from reservation where user_id=1'
    # with Dbsql('db') as db:
    #     res = db.fetch_oll(a)
    table = 'reservation'
    colons = 'service_id'
    condition = {'user_id': user_id}

    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition)
        print(res)
    # return res
    return render_template("reservations.html", res = res)

@app.post('/delete_reservation/<reservation_id>')

def delete_reservation(reservation_id):
    user_id = session.get('user_id', None)
    from_data = request.form
    service_id = from_data.get('service_id')
    print(service_id)

    table = 'reservation'
    condition = {'user_id': user_id, 'service_id' : service_id }
    print(table, condition)
    with Dbsql('db') as db:
        db.delete_from_db(table, condition)
    return redirect('/')

@app.get('/reservations/<reservation_id>')
@login_required

def user_reservations_info(reservation_id):
    user_id = session.get('user_id', None)

    # a = f'select * from reservation where user_id=1'
    # with Dbsql('db') as db:
    #     res = db.fetch_oll(a)
    table = 'reservation'
    colons = None
    condition = {'user_id': user_id}
    with Dbsql('db') as db:

        res = db.fetch_oll(table, colons, condition)
    # return res

    return render_template("reservation_id.html", reservation_id=reservation_id, res = res)


@app.put('/reservations/<reservation_id>')
def update_reservations(reservation_id):
    return f'reservations {reservation_id} was successfully updated'


@app.delete('/reservations/<reservation_id>')
def delete_reservations(reservation_id):
    return f'user reservations {reservation_id} was successfully deleted'


@app.post('/checkout')
def add_checkout_order_service():
    return 'add checkout order service'


@app.get('/checkout')
def checkout_info():
    # a = f'select name, price from service '
    # with Dbsql('db') as db:
    #     res = db.fetch_oll(a)
    table = 'service'
    colons = ['name', 'price']
    condition = None
    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition)
    return render_template("checkout.html", res = res)


@app.put('/checkout')
def update_checkout_order_service():
    return 'checkout order service was successfully updated'


@app.get('/fitness_center')
def get_fitness_center():
    # a = 'select name, address from fitness_center'
    # with Dbsql('db') as db:
    #     res = db.fetch_oll(a)
    table = 'fitness_center'
    colons = ['name_fc', 'address','id']
    condition = None
    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition)
        print(type(res),res)
    return render_template("fitness_center.html", res = res)

@app.get('/fitness_center/<gym_id>')
def get_fitness_center_info(gym_id):
    # table = 'fitness_center'
    # conditions =
    # a = f'select name, address from fitness_center where id={gym_id}'
    table = 'fitness_center'
    colons = None
    condition = {'fitness_center.id': gym_id}
    join_condition = {'fitness_center_id': gym_id}
    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition, join_table = ['trainer'],join_condition=join_condition)
        print(res)
    table = 'fitness_center'
    colons = None
    condition = {'fitness_center.id': gym_id}
    join_condition = {'fitness_center_id': gym_id}
    with Dbsql('db') as db:
        res_s = db.fetch_oll(table, colons, condition, join_table=['service'], join_condition=join_condition)
        print(res_s)
    return render_template("gym_id.html", res = res, res_s = res_s, gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/service')
def get_service(gym_id):
    a = f'select name from service where fitness_center_id={gym_id}'
    # with Dbsql('db') as db:
    #     res = db.fetch_oll(a)
    table = 'service'
    colons = ['name']
    condition = {'fitness_center_id': gym_id}
    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition)

    return render_template("service.html", res = res, gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/service/<service_id>')
def get_service_info(gym_id, service_id):
    # a = f'select * from service where fitness_center_id={gym_id} AND id={service_id}'
    # with Dbsql('db') as db:
    #     res = db.fetch_oll(a)
    table = 'service'
    colons = None
    condition = {'fitness_center_id': gym_id, 'service.id': service_id}
    join_condition = {'service_id': service_id}

    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition, join_table=['trainer_service'], join_condition=join_condition)

    return render_template("service_id.html", res = res, service_id=service_id, gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/trainer')
def get_trainer(gym_id):

    table = 'trainer'
    colons = ['name']
    condition = {'fitness_center_id': gym_id}
    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition)

    return render_template("trainer.html", res = res,  gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/trainer/<trainer_id>')
def get_coach_info(gym_id, trainer_id):

    table = 'trainer'
    colons = None
    condition = {'fitness_center_id': gym_id, 'trainer.id': trainer_id}
    join_condition = {'trainer_id': trainer_id}

    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition, join_table=['trainer_service'], join_condition=join_condition)

    return render_template("trainer_id.html", res = res, trainer_id=trainer_id, gym_id=gym_id)


@app.get('/fitness_center/<gym_id>/trainer/<trainer_id>/score')
@login_required

def get_coach_score(gym_id, trainer_id):
    print(gym_id, trainer_id)
    return render_template('score.html', gym_id=gym_id, trainer_id=trainer_id)




@app.post('/fitness_center/<gym_id>/trainer/<trainer_id>/score')
def set_coach_score(gym_id, trainer_id):
    user_id = session.get('user_id', None)
    from_data = request.form
    table_bd = "review_rating"
    k_r = {'user_id': user_id, 'point': from_data['point'], 'text': from_data['text'], 'trainer_id': from_data['trainer_id'], 'gym_id': from_data['gym_id']}
    with Dbsql('db') as db:
        table = 'review_rating'
        colons = None
        condition = {'gym_id': from_data['gym_id'], 'trainer_id': from_data['trainer_id'], 'user_id': user_id}
        res = db.fetch_one(table, colons, condition)
        if res is None:
            db.insert_to_db(table_bd, k_r)
            return render_template('score_add.html', gym_id=from_data['gym_id'], trainer_id=from_data['trainer_id'])
        else:
            db.update_db(table=table_bd, data=k_r, condition=condition)
            return render_template('score_add.html', gym_id=from_data['gym_id'], trainer_id=from_data['trainer_id'])


@app.put('/fitness_center/<gym_id>/trainer/<trainer_id>/score')
def update_coach_score(gym_id, trainer_id):
    return f'fitness center {gym_id} trainer {trainer_id} score was updated'


@app.get('/fitness_center/<gym_id>/loyality_programs')
def get_loyality_programs(gym_id):

    table = 'fitness_center'
    colons = ['name']
    condition = {'id': gym_id}
    with Dbsql('db') as db:
        res = db.fetch_oll(table, colons, condition)
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


@app.get('/pre_reservation')
@login_required

def pre_reservation_2():
    user_id = session.get('user_id', None)
    trainer = request.args.get('gym_id', '')
    service = request.args.get('trainer_id', '')
    # from_data = request.form
    # trainer = from_data['trainer_id']
    # service = from_data['service_id']
    desired_date = '31.05.2024'#from_data['desired_date']

    time_slots = clac_slots(trainer, service), #@desired_date)
    return render_template("pre_reservation.html", form_info={'trainer_id':trainer, 'service_id':service, 'desired_date':desired_date, 'time_slots':time_slots})

if __name__ == '__main__':
    app.run()
