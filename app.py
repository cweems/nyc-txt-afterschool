import os
import requests
import operator
from collections import namedtuple
import re
from flask import Flask, render_template, request, jsonify
import urllib.request
from flask.ext.sqlalchemy import SQLAlchemy
from geopy.distance import vincenty

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print (os.environ['DATABASE_URL'])
from models import Result


@app.route('/api/<location>')
def find_location(location):
	results = [];
	errors = [];
	#print(location)
	if(re.match('\d{5}(-\d{4})?$', location)):
		print(location)
		for row in db.session.query(Result).filter(Result.site_zip == location).all():
			results.append(row.site_name)
			print(row.site_name)
	else:
		mapzen_api_key = app.config['MAPZEN_API_KEY']
		boundary_lattitude = app.config['LOCATION_LAT']
		boundary_longitude = app.config['LOCATION_LONG']
		radius = app.config['LOCATION_RADIUS_KM']

		url = "https://search.mapzen.com/v1/search?text=" + location + "&api_key=" + mapzen_api_key + "&boundary.circle.lat=" + boundary_lattitude + "&boundary.circle.lon=" + boundary_longitude + "&boundary.circle.radius=" + radius + "&size=1"
		try:
			req = requests.get(url)
			results = req.json()
			lat_lon = results['features'][0]['geometry']['coordinates']
			lat = lat_lon[1]
			lon = lat_lon[0]

			results = []
			less_than_a_mile = []

			user_location = (lat, lon)
			print(user_location)
			for row in db.session.query(Result).all():
				program_location = (row.lat, row.lon)
				index = row.id
				name = row.program_name
				borough = row.site_borough
				distance = vincenty(user_location, program_location).miles
				ResponseStructure = namedtuple('ResponseStructure', 'idNumber name borough distance')

				entry = ResponseStructure(idNumber=index, name=name, borough=borough, distance=distance)
				results.append(entry)

			sorted_results = sorted(results, key=lambda entry: entry[3])
			top_three_results = sorted_results[0:3]
			print(top_three_results)
			return jsonify(results=top_three_results);
		except:
			return "unable to find that address"

		#, name=top_three_results.name, borough=top_three_results.borough, distance=top_three_results.distance

		#name=top_three_results[2], borough=top_three_results[3], distance=top_three_results[4]
	return render_template('/index.html', errors = errors, results = results)

@app.route('/', methods=['GET', 'POST'])
def index():
	errors = []
	results = []
	if request.method == 'POST':
		try:
			zipcode = request.form['zipcode']
			print(zipcode)
		except:
			errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
			return render_template('index.html', errors = errors)
		if zipcode:
			for row in db.session.query(Result).filter(Result.site_zip == zipcode).all():
				results.append([row.site_name, row.address1])
				print(results)
	return render_template('/index.html', errors = errors, results = results)

@app.route('/twilio', methods=['GET', 'POST'])
def sms_test():
	resp = twilio.twiml.Response()
	resp.message("Hello, the text worked")
	return str(resp)

if __name__ == '__main__':
	app.run()
