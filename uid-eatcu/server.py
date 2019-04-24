from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)


restaurants = []

appointments = []

restaurants_index = len(restaurants);

appointments_index = len(appointments);

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
                "index": restaurants_index,
                "id": id,
                "title": title,
                "address": address,
                "icon": icon,
                "position": position
            }

            restaurants_index +=1
            restaurants.append(new_item_entry)

        else :

            json_data = request.get_json()
            id = json_data["id"]
            title = json_data["title"]
            date = json_data["date"]
            starttime = json_data["starttime"]
            endtime = json_data["endtime"]
            notes = json_data["notes"]


            new_item_entry = {
                "index": appointments_index,
                "id": id,
                "title": title,
                "date": date,
                "starttime": starttime,
                "endtime": endtime,
                "notes": notes
            }

            appointments_index += 1
            appointments.append(new_item_entry)

        return jsonify(restaurants = restaurants, appointments = appointments)
    else:
        return render_template('search.html', appointments = appointments, restaurants = restaurants, restaurants_index = restaurants_index, appointments_index = appointments_index)

if __name__ == '__main__':
    app.run(debug = True)