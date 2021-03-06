'''
Title
------
utils.py

Description
------------
Helper methods

'''

import datetime
import re
import random
import string
import requests
import json

'''
Validate member object, check if all required fields
are completed and in the correct format
'''
def validateMember(memberObj, edit, club_names):
    if not type(memberObj) is dict:
        raise Exception('Invalid input for validateMember function')
    if "general" not in memberObj:
        raise Exception('member invalid: must contain general form values')
    if "enrollment_form" not in memberObj:
        raise Exception('member invalid: must contain enrollment form values')
    if "demographic_data" not in memberObj:
        raise Exception('member invalid: must contain demographic data values')
    if "self_sufficiency_matrix" not in memberObj:
        raise Exception('member invalid: must contain self sufficiency matrix values')
    if "self_efficacy_quiz" not in memberObj:
        raise Exception('member invalid: must contain self efficacy quiz values')
    # validate general
    general = validateGeneral(memberObj['general'], edit, club_names)
    general['form'] = 'general'
    if general["success"] == False:
        return general
    # validate enrollment form
    enrollment_form = validateEnrollmentForm(memberObj['enrollment_form'])
    enrollment_form['form'] = 'enrollment_form'
    if enrollment_form["success"] == False:
        return enrollment_form
    # validate demographic data
    demographic_data = validateDemographicData(memberObj['demographic_data'])
    demographic_data['form'] = 'demographic_data'
    if demographic_data["success"] == False:
        return demographic_data
    # validate self sufficiency matrix
    self_sufficiency_matrix = validateSelfSufficiencyMatrix(memberObj['self_sufficiency_matrix'])
    self_sufficiency_matrix['form'] = 'self_sufficiency_matrix'
    if self_sufficiency_matrix["success"] == False:
        return self_sufficiency_matrix
    # validate self efficacy quiz
    self_efficacy_quiz = validateSelfEfficacyQuiz(memberObj['self_efficacy_quiz'])
    self_efficacy_quiz['form'] = 'self_efficacy_quiz'
    if self_efficacy_quiz["success"] == False:
        return self_efficacy_quiz
    return {"success":True, "error":None}

'''
Validate general portion of member object
'''
def validateGeneral(general, edit, club_names):
    date_string = "%Y-%m-%d"
    if general == {}:
        return {"success":False, "error":"general form must be filled out"}
    if not edit and \
            ('username' not in general or general['username'] == ''):
        return {"success":False, "error":"Username can not be blank"}
    elif not edit and len(general['username']) < 5:
        return {"success":False, "error":"Username must be greater than 5 characters"}
    elif not edit and len(general['password']) < 6:
        return {"success":False, "error":"Password must be 6 or more characters"}
    # TODO: check club name against clubs in database as well
    elif general['club_name'] == '':
        return {"success":False, "error":"Club Name must not be blank"}
    elif general['club_name'] not in club_names:
        return {"success":False, "error":"Club Name does not exist"}
    elif general['join_date'] == '':
        return {"success":False, "error":"Must select join date"}
    elif datetime.datetime.strptime(general['join_date'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Join date must not be in the future"}
    elif general['photo_release'] == '':
        return {"success":False, "error":"Must select date for Photo Release Signature"}
    elif datetime.datetime.strptime(general['photo_release'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Photo Release sign date must not be in the future"}
    elif general['commitment_pledge'] == '':
        return {"success":False, "error":"Must select date for Commitment Pledge Signature"}
    elif datetime.datetime.strptime(general['commitment_pledge'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Commitment Pledge sign date must not be in the future"}
    return {"success":True, "error":None}

'''
Validate enrollment form portion of member object
'''
def validateEnrollmentForm(enrollment_form):
    date_string = "%Y-%m-%d"
    if enrollment_form == {}:
        return {"success":False, "error":"Enrollment form must be filled out"}
    elif enrollment_form['first_name'] == '':
        return {"success":False, "error":"Member must have a first name"}
    elif enrollment_form['last_name'] == '':
        return {"success":False, "error":"Member must have a last name"}
    elif enrollment_form['address_street'] == '':
        return {"success":False, "error":"Address street name can not be blank"}
    elif enrollment_form['address_city'] == '':
        return {"success":False, "error":"Address city can not be blank"}
    elif enrollment_form['address_zip'] == '':
        return {"success":False, "error":"Address zip code can not be blank"}
    elif not re.match('^\d{5}(?:[-\s]\d{4})?$', enrollment_form['address_zip']):
        return {"success":False, "error":"Invalid Zip Code"}
    elif enrollment_form['birth_date'] == '':
        return {"success":False, "error":"Birth Date must not be blank"}
    elif datetime.datetime.strptime(enrollment_form['birth_date'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Birth date must not be in the future"}
    elif enrollment_form['phone_numbers'][0] == '' and len(enrollment_form['phone_numbers']) == 1:
        return {"success":False, "error":"Must include at least 1 phone number"}
    elif enrollment_form['email'] != '' and not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', enrollment_form['email']):
        return {"success":False, "error":"Invalid email address"}
    for number in enrollment_form['phone_numbers']:
        if not re.match('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', number):
            return {"success":False, "error":"Phone numbers must be in a valid format"}
    for child in enrollment_form['children']:
        if child['child_first_name'] == '':
            return {"success":False, "error":"Child first name must not be blank"}
        elif child['child_last_name'] == '':
            return {"success":False, "error":"Child last name must not be blank"}
        elif child['child_birth_date'] == '':
            return {"success":False, "error":"Child birth date must not be blank"}
    return {"success":True, "error":None}


'''
Validate demographic data portion of member object
'''
def validateDemographicData(demographic_data):
    if demographic_data == {}:
        return {"success":False, "error":"Demographic Data must be filled out"}
    if 'race' not in demographic_data:
        return {"success":False, "error":"Race is a required field"}
    if 'marital_status' not in demographic_data:
        return {"success":False, "error":"Marital Status is a required field"}
    if 'education' not in demographic_data:
        return {"success":False, "error":"Education is a required field"}
    if 'employment_status' not in demographic_data:
        return {"success":False, "error":"Employment is a required field"}
    return {"success":True, "error":None}

'''
Validate self sufficiency matrix portion of member object
'''
def validateSelfSufficiencyMatrix(self_sufficiency_matrix):
    return {"success":True, "error":None}

'''
Validate self efficacy quiz portion of member object
'''
def validateSelfEfficacyQuiz(self_efficacy_quiz):
    return {"success":True, "error":None}

'''
Validate goal object
'''
def validateGoal(goal):
    # TODO: finish validate goal function
    for step in goal['steps']:
        if step['step_name'] == '':
            return {"success":False, "error":"Step Name can not be blank"}
    return {"success":True, "error":None}

'''
Validate club object
Check if the address is valid (can be geocoded)
'''
def validateClub(club, coordinators):
    # TODO: finish validate club function
    for coordinator in club['coordinators']:
        if coordinator not in coordinators:
            return {"success":False, "error":"Coordinator with username: " + coordinator + " does not exist", "club":None}
    if 'address_street' not in club:
        return {"success":False, "error":"Club must have street address", "club":None}
    coord = validateClubAddress(club)
    if coord["success"] == False:
        return {"success":False, "error":"Invalid club address", "club":None}
    club['latitude'] = coord['latitude']
    club['longitude'] = coord['longitude']
    club['county'] = coord['county']
    return {"success":True, "error":None, "club":club}

def validateClubAddress(club):
    club_address = club['address_street'] + ' ' + club['address_city'] + ', ' + club['address_state'] + ' ' + club['address_zip']
    return getCoordinatesAndCounty(club_address)

def getAddress(club):
    club_address = club['address_street'] + ' ' + club['address_city'] + ', ' + club['address_state'] + ' ' + club['address_zip']
    return club_address

'''
Return complete list of abbreviated US States
'''
def getStates():
    return ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

'''
Use the Google Geocoding API to get the location
and county of an address
'''
def getCoordinatesAndCounty(address):
    query_address_list = address.split(' ')
    query_address = '+'.join(query_address_list)
    apikey = 'AIzaSyAOZ9KV5NeXE2_Bw6G0Ot4OebKi1WSu3y4'
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + query_address + '&key=' + apikey)
    resp_json_payload = response.json()
    if len(resp_json_payload['results']) == 0:
        return {'latitude': None, 'longitude': None, 'county': None, 'success': False}
    lat = resp_json_payload['results'][0]['geometry']['location']['lat']
    long = resp_json_payload['results'][0]['geometry']['location']['lng']
    county = None
    for x in resp_json_payload['results'][0]['address_components']:
        if 'administrative_area_level_2' in x['types']:
            county = x['long_name']
    return {'latitude': lat, 'longitude': long, 'county': county, 'success': True}

'''
convert sqlalchemy query to dict
'''
def toDict(query):
    results = {}
    for x in query:
        if is_jsonable(query[x]):
            results[x] = query.x
        else:
            results[x] = toDict(query.x)
    return results

'''
Check if object is jsonable
'''
def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False

'''
Remove all non-ascii characters in a string s
'''
def remove_non_ascii(s):
    if type(s) == str:
        return  "".join([x if ord(x) < 128 else '?' for x in s])
    else:
        return s

def generate_password():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
