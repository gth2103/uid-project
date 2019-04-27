from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from app import app, db
from app.models import *
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required

restaurants = []

appointments = []

restaurants_index = len(restaurants);

appointments_index = len(appointments);


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form  = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form  = RegistrationForm()
    if form.validate_on_submit():
        commit_registration(form)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    global restaurants
    global appointments
    global restaurants_index
    global appointments_index

    appointment = request.args.get('appointment')
   
    if request.method == 'POST':
        print(appointment)
        if (appointment == 'false') :

            json_data = request.get_json()
            id = json_data["id"]
            title = json_data["title"]
            address = json_data["address"]
            icon = json_data["icon"]
            position = json_data["position"]

            new_item_entry = {
                "id": id,
                "title": title,
                "address": address,
                "icon": icon,
                "position": position
            }

            restaurants_index +=1

            if new_item_entry not in restaurants:
                restaurants.append(new_item_entry)

        else :

            json_data = request.get_json()
            id = json_data["id"]
            title = json_data["title"]
            date = json_data["date"]
            starttime = json_data["starttime"]
            endtime = json_data["endtime"]
            notes = json_data["notes"]
            address = json_data["address"]


            new_item_entry = {
                "id": id,
                "title": title,
                "date": date,
                "starttime": starttime,
                "endtime": endtime,
                "notes": notes,
                "address": address
            }

            appointments_index += 1
           

 
            if new_item_entry not in appointments:
                appointments.append(new_item_entry)

            print(appointments)
        return jsonify(restaurants = restaurants, appointments = appointments)
    else:
        return render_template('search.html', appointments = appointments, restaurants = restaurants, restaurants_index = restaurants_index, appointments_index = appointments_index)

@app.route('/item', methods=['GET'])
def item():
    global appointments
    return render_template('item.html', appointments = appointments);

if __name__ == '__main__':
    app.run(debug = True)
