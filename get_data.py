import os
import sys
import logging
import requests
import json

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from app import app, db
from models import Result

try:
    url = 'https://data.cityofnewyork.us/resource/reni-g9vg.json'
    r = requests.get(url)

    data = json.loads(r.text)
    for afterschool_program in data:

        if afterschool_program['academics'].lower() == 'yes':
            academics = True
        else:
            academics = False
        print(academics)

        address1 = afterschool_program['address1']
        print(address1)

        address2 = afterschool_program['address2']
        print(address2)

        agency_name = afterschool_program['agency_nam']
        print(agency_name)

        agency_tel = afterschool_program['agency_tel']
        print(agency_tel)

        if afterschool_program['arts_cultu'].lower() == 'yes':
            arts_culture = True
        else:
            arts_culture = False
        print(arts_culture)

        cbo_service = afterschool_program['cbo_servic']
        print(cbo_service)

        cbo_sp_tel = afterschool_program['cbo_sp_tel']
        print(cbo_sp_tel)

        if afterschool_program['elementary'].lower() == 'yes':
            elementary = True
        else:
            elementary = False
        print(elementary)

        if afterschool_program['enrollment'].isdigit():
            enrollment = int(float(afterschool_program['enrollment']))
        else:
            enrollment = 0
        print(enrollment)

        if afterschool_program['estimated_'].isdigit():
            estimated = int(float(afterschool_program['estimated_']))
        else:
            estimated = 0
        print(estimated)

        if afterschool_program['evenings'].lower() == 'yes':
            evenings = True
        else:
            evenings = False
        print(evenings)

        if afterschool_program['high_schoo'].lower() == 'yes':
            high_school = True
        else:
            high_school = False
        print(high_school)

        site_id = afterschool_program['id']
        print(site_id)

        #Issue! Needs to be Bool
        if afterschool_program['middle_sch'].lower() == 'yes':
            middle_school = True
        else:
            middle_school = False
        print(middle_school)

        program_name = afterschool_program['name']
        print(program_name)

        program_ty = afterschool_program['program_ty']
        print(program_ty)

        school_id = afterschool_program['school_id']
        print(school_id)

        if afterschool_program['school_yea'].lower() == 'yes':
            school_year = True
        else:
            school_year = False
        print(school_year)

        setting = afterschool_program['setting']
        print(setting)

        site_borough = afterschool_program['site_borou']
        print(site_borough)

        site_building = afterschool_program['site_build']
        print(site_building)

        site_name = afterschool_program['site_name']
        print(site_name)

        site_street = afterschool_program['site_stree']
        print(site_street)

        site_zip = int(float(afterschool_program['site_zip']))
        print(site_zip)

        if afterschool_program['sp_ein'].isdigit():
            sp_ein = int(afterschool_program['sp_ein'])
        else:
            sp_ein = None
        print(sp_ein)

        if afterschool_program['sports_phy'].lower() == 'yes':
            sports_phy = True
        else:
            sports_phy = False
        print(sports_phy)

        if afterschool_program['summer'].lower() == 'yes':
            summer = True
        else:
            summer = False
        print(summer)

        geometry = afterschool_program['the_geom']['type']
        print(geometry)

        lat = float(afterschool_program['the_geom']['coordinates'][1])
        print(lat)

        lon = float(afterschool_program['the_geom']['coordinates'][0])
        print(lon)

        if afterschool_program['weekends'].lower() == 'yes':
            weekends = True
        else:
            weekends = False
        print(weekends)

        weekly_hours = afterschool_program['weekly_hou']
        print(weekly_hours)


        try:
            result = Result(
                academics = academics,
                address1 = address1,
                address2 = address2,
                agency_name = agency_name,
                agency_tel = agency_tel,
                arts_culture = arts_culture,
                cbo_service = cbo_service,
                cbo_sp_tel = cbo_sp_tel,
                elementary = elementary,
                enrollment = enrollment,
                estimated = estimated,
                evenings = evenings,
                high_school = high_school,
                site_id = site_id,
                middle_school = middle_school,
                program_name = program_name,
                program_ty = program_ty,
                school_id = school_id,
                school_year = school_year,
                setting = setting,
                site_borough = site_borough,
                site_building = site_building,
                site_name = site_name,
                site_street = site_street,
                site_zip = site_zip,
                sp_ein = sp_ein,
                sports_phy = sports_phy,
                summer = summer,
                geometry = geometry,
                lat = lat,
                lon = lon,
                weekends = weekends,
                weekly_hours = weekly_hours
            )
            db.session.add(result)
            db.session.commit()
        except:
            print ("Unable to add item to database.")
            logging.exception('Got exception on main handler')
            raise

except:
    print ("Unexpected error:", sys.exc_info())
    logging.exception('Got exception on main handler')
    raise
