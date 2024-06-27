from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_bounds', methods=['POST'])
def save_bounds():
    data = request.json
    with open('map_bounds.csv', 'w', newline='') as csvfile:
        fieldnames = ['corner', 'latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'corner': 'northEast', 'latitude': data['northEast']['lat'], 'longitude': data['northEast']['lng']})
        writer.writerow({'corner': 'northWest', 'latitude': data['northWest']['lat'], 'longitude': data['northWest']['lng']})
        writer.writerow({'corner': 'southEast', 'latitude': data['southEast']['lat'], 'longitude': data['southEast']['lng']})
        writer.writerow({'corner': 'southWest', 'latitude': data['southWest']['lat'], 'longitude': data['southWest']['lng']})

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
