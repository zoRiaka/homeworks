# Main app module
# create and parse different html forms
from flask import Flask, render_template, request
from main_functions import *
app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    return render_template('index_1.html')

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        choice = request.form['opt']
        if choice == "1":
            return render_template('index_2.html')
        elif choice == "2":
            return render_template('index_3.html')

    return render_template('index_1.html')

@app.route('/sendmap', methods=['POST'])
def sendmap():
    if request.method == 'POST':
        choice = request.form['opt']
        if choice == "1":
            overallmap_gener()
            return render_template('overall_map.html')
        elif choice == "2":
            return render_template('centralized_coordinates.html')

    return render_template('index_2.html')

@app.route('/sendcoordinates', methods=['POST'])
def sendmapcoordinates():
    if request.method == 'POST':
        coordinates = request.form['name']
        map_gener(coordinates)
        return render_template('centralized_map.html')

    return render_template('centralized_coordinates.html')


@app.route('/sendinfo', methods=['POST'])
def sendinfo():
    if request.method == 'POST':
        choice = request.form['opt']
        if choice == "1":
            return render_template('enter_species.html')
        elif choice == "2":
            return render_template('enter_speciesKey.html')
        elif choice == "3":
            return render_template('enter_id.html')


    return render_template('index_3.html')


@app.route('/sendspecies', methods=['POST'])
def sendspecies():
    if request.method == 'POST':
        specie = request.form['name']
        view_by('species', specie)
        return render_template(f'{specie}_table.html')

    return render_template('enter_species.html')

@app.route('/sendspeciesKey', methods=['POST'])
def sendspeciesKey():
    if request.method == 'POST':
        specieKey = str(request.form['name'])
        view_by('speciesKey', specieKey)
        return render_template(f'{specieKey}_table.html')

    return render_template('enter_speciesKey.html')

@app.route('/sendid', methods=['POST'])
def sendid():
    if request.method == 'POST':
        id = str(request.form['name'])
        view_by('gbifID', id)
        return render_template(f'{id}_table.html')

    return render_template('enter_id.html')


if __name__ == "__main__":
    app.run()
