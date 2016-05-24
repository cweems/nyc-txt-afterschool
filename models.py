from app import db
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
    __tablename__ = 'afterschool_programs'

    id = db.Column(db.Integer, primary_key=True)

    academics = db.Column(db.Boolean())
    address1 = db.Column(db.String())
    address2 = db.Column(db.String())
    agency_name = db.Column(db.String())
    agency_tel = db.Column(db.String())
    arts_culture = db.Column(db.Boolean())
    cbo_service = db.Column(db.String())
    cbo_sp_tel = db.Column(db.String())
    elementary = db.Column(db.Boolean())
    enrollment = db.Column(db.Integer())
    estimated = db.Column(db.Integer())
    evenings = db.Column(db.Boolean())
    high_school = db.Column(db.Boolean())
    site_id = db.Column(db.String())
    middle_school = db.Column(db.Boolean())
    program_name = db.Column(db.String())
    program_ty = db.Column(db.String())
    school_id = db.Column(db.String())
    school_year = db.Column(db.Boolean())
    setting = db.Column(db.String())
    site_borough = db.Column(db.String())
    site_building = db.Column(db.String())
    site_name = db.Column(db.String())
    site_street = db.Column(db.String())
    site_zip = db.Column(db.Integer())

    #Will need to catch N/A
    sp_ein = db.Column(db.Integer())
    sports_phy = db.Column(db.Boolean())

    #Yes, No, Unknown
    summer = db.Column(db.Boolean())

    geometry = db.Column(db.String())
    lat = db.Column(db.Integer())
    lon = db.Column(db.Integer())

    weekends = db.Column(db.Boolean())
    weekly_hours = db.Column(db.String())

    def __init__(
            self,
            address1,
            address2,
            agency_name,
            agency_tel,
            arts_culture,
            cbo_service,
            cbo_sp_tel,
            elementary,
            enrollment,
            estimated,
            evenings,
            high_school,
            site_id,
            middle_school,
            program_name,
            program_ty,
            school_id,
            school_year,
            setting,
            site_borough,
            site_building,
            site_name,
            site_street,
            site_zip,
            sp_ein,
            sports_phy,
            summer,
            geometry,
            lat,
            lon,
            weekends,
            weekly_hours
        ):
        self.academics = academics
        self.address1 = address1
        self.address2 = address2
        self.agency_name = agency_name
        self.agency_tel = agency_tel
        self.arts_culture = arts_culture
        self.cbo_service = cbo_service
        self.cbo_sp_tel = cbo_sp_tel
        self.elementary = enrollment
        self.estimated = estimated
        self.evenings = evenings
        self.high_school = high_school
        self.site_id = site_id
        self.middle_school = middle_school
        self.program_name = program_name
        self.program_ty = program_ty
        self.school_id = school_id
        self.school_year = school_year
        self.setting = setting
        self.site_borough = site_borough
        self.site_building = site_building
        self.site_name = site_name
        self.site_street = site_street
        self.site_zip = site_zip
        self.sp_ein = sp_ein
        self.sports_phy = sports_phy
        self.summer = summer
        self.geometry = geometry
        self.lat = lat
        self.lon = lon
        self.weekends = weekends
        self.weekly_hours

    def __repr__(self):
        return '<id {}>'.format(self.id)
