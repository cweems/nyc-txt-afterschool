import os
import requests
import operator
import math
from collections import namedtuple
import re
from flask import Flask, render_template, request, jsonify, session
import urllib.request
from flask.ext.sqlalchemy import SQLAlchemy
from geopy.distance import vincenty
import twilio.twiml

print(os.environ['SESSION_SECRET'])

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.secret_key = os.environ['SESSION_SECRET']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print (os.environ['DATABASE_URL'])
from models import Result

def calculate_distance(user_location, program_location):
	distance = vincenty(user_location, program_location).miles
	return(distance)

def format_response(row, user_location):
	index = row.id
	program_location = (row.lat, row.lon)
	name = row.program_name
	address = row.address1
	borough = row.site_borough
	distance = calculate_distance(user_location, program_location)
	telephone = row.cbo_sp_tel
	miles = math.ceil(distance*100)/100
	message = (name + " Addr: " + address + " " + borough + " Distance: " + str(miles) + "mi. Call: " + telephone)
	entry = {
		"idNumber": index,
		"name": name,
		"address": address,
		"borough": borough,
		"distance": distance,
		"telephone": telephone,
		"message": message
	}
	return entry;

def sorted_results_function(results):
	test_to_return = sorted(results, key=lambda entry: entry['distance'])
	return test_to_return

def paginate_results(results, start, stop):
	return results[start:stop]

def geocode(location_string):
	mapzen_api_key = app.config['MAPZEN_API_KEY']
	boundary_lattitude = app.config['LOCATION_LAT']
	boundary_longitude = app.config['LOCATION_LONG']
	radius = app.config['LOCATION_RADIUS_KM']

	url = "https://search.mapzen.com/v1/search?text=" + location_string + "&api_key=" + mapzen_api_key + "&boundary.circle.lat=" + boundary_lattitude + "&boundary.circle.lon=" + boundary_longitude + "&boundary.circle.radius=" + radius + "&size=1"
	try:
		req = requests.get(url)
		results = req.json()
		lat_lon = results['features'][0]['geometry']['coordinates']
		lat = lat_lon[1]
		lon = lat_lon[0]

		results = []

		user_location = (lat, lon)

		print(user_location)
		for row in db.session.query(Result).all():

			entry = format_response(row, user_location)

			results.append(entry)

		sorted_results = sorted_results_function(results)
		top_three_results = paginate_results(sorted_results, 0, 3)
		return top_three_results;
	except:
		errors.append('Geocoding failed. Check that Mapzen API Key is configured correctly.')
		return render_template('/index.html', errors = errors, results = results)

#Currently does same thing for addresses and zip-codes, keeping in case we want an analytics event
def location_type(location_string):
	if(re.match('\d{5}(-\d{4})?$', location_string)):
		results = geocode(location_string)
		return results
	else:
		results = geocode(location_string)
		return results

@app.route('/api/<location>')
def location(location):
	location = find_location(location)
	return jsonify(result=location)

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

@app.route('/sms/', methods=['GET', 'POST'])
def sms_test():
	total_count = session.get('counter', 0)
	from_number = request.values.get('From', None)
	message = str(request.values.get('Body'))
	resp = twilio.twiml.Response()
	print(message)
	if(message):
		returned_results = location_type(message)
		counter = 0
		for item in returned_results:
			counter += 1
			total_count += 1
			session['total_count'] = total_count
			resp.message(str(counter) + ') ' + item['message'] + ' Results sent: ' + str(total_count))
	else:
		resp.message("Sorry, we couldn't understand that address. Try entering another address or zip-code located in NYC.")


	return str(resp)

if __name__ == '__main__':
	app.run()
