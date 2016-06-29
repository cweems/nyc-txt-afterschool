import os
import requests
import operator
import math
from collections import namedtuple
import re
from flask import Flask, render_template, request, jsonify
import urllib.request
from flask.ext.sqlalchemy import SQLAlchemy
from geopy.distance import vincenty
import twilio.twiml

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print (os.environ['DATABASE_URL'])
from models import Result

#school_year, summer, weekends, distance, telephone
def format_response(name, address, borough, distance, telephone):
	miles = math.ceil(distance*100)/100
	message = ("Name: " + name + " Addr: " + address + " " + borough + " Distance: " + str(miles) + "mi. Call: " + telephone)
	return message;

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

			user_location = (lat, lon)
			print(user_location)
			for row in db.session.query(Result).all():
				program_location = (row.lat, row.lon)
				index = row.id
				name = row.program_name
				address = row.address1
				borough = row.site_borough
				distance = vincenty(user_location, program_location).miles
				telephone = row.cbo_sp_tel
				message = format_response(name, address, borough, distance, telephone)
				entry = {
					"idNumber": index,
					"name": name,
					"address": address,
					"borough": borough,
					"distance": distance,
					"telephone": telephone,
					"message": message
				}

				results.append(entry)

			sorted_results = sorted(results, key=lambda entry: entry['distance'])
			top_three_results = sorted_results[0:1]
			return top_three_results;
		except:
			errors.append('Geocoding failed. Check that Mapzen API Key is configured correctly.')
			return render_template('/index.html', errors = errors, results = results)

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
	from_number = request.values.get('From', None)
	message = str(request.values.get('Body'))
	resp = twilio.twiml.Response()
	print(message)
	if(message):
		returned_results = find_location(message)
		resp.message(returned_results[0]['message'])
	else:
		resp.message("No address found!")


	return str(resp)

if __name__ == '__main__':
	app.run()
