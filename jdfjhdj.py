
import twitter2
import folium
import certifi
import ssl
import geopy
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


class_you_need = 'location'
js = set()
# with open(path, encoding='utf-8') as f:
#     data = json.load(f)

def reading_json(data1, class_you_need1):
    """
    (str) -> (dict)
    this function creates a dictionary that contains information
    about group, division and section of a class that user gives us 
    as an input
    """
    if type(data1) is dict:
        for key in data1:
            if key == class_you_need1:
                js.add((data1[key], data1['screen_name']))
            reading_json(data1[key], class_you_need1)
    if type(data1) is list:
        for i in data1:
            reading_json(i, class_you_need1)
    return js
# print(reading_json(data, class_you_need))

# js = reading_json(data, class_you_need)
@app.route('/12', methods=['POST'])

def creating_map():
    user_name = str(request.form['name'])
    data = twitter2.create_js(user_name)
    js = reading_json(data, class_you_need)
    dict_locations = {}
    list_empty = []
    geolocator = Nominatim(user_agent="main.py")
    for i in js:
        if i[0] == '':
            list_empty.append(i)
        else:
            location = geolocator.geocode(i[0])
            try:
                dict_locations[i[1]] = (location.latitude, location.longitude)
            except AttributeError:
                list_empty.append(i)
    m = folium.Map(location=[49, 24], zoom_start=11)
    for key in dict_locations:
        folium.Marker(list(dict_locations[key]), popup='my_point', tooltip=key).add_to(m)
    n = m.get_root().render()
    contex = {"n": n}

    return render_template('map.html', **contex)

if __name__ == '__main__':
    app.run(debug=True)