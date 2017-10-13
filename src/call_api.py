import requests
import xmltodict
from _datetime import datetime

apis = {"timetables": {"url": "https://api.deutschebahn.com/timetables/v1/",
                       "return": "xml"},
        "fahrplan-plus": {"url": "https://api.deutschebahn.com/fahrplan-plus/v1/",
                          "return": "json"}
        }
cancel_states = {"a": "added", "c": "cancelled", "p": "planned"}
headers = {'Authorization': 'Bearer e9e44e33b8db8147fc5cb03e5df2beb2'}

dt = datetime.now()
date = dt.strftime('%y%m%d')
hour = dt.hour

def parse_ar(ride):
    out = {}
    if 'ar' in ride:
        if '@l' in ride['ar']:
            out['ankunft']['line'] = ride['ar']['@l']
        #out['ankunft']['zeitGeplant'] = ride['ar']['@pt']
        #if '@pt' in ride['ar']:
        #    out['ankunft']['zeitAktuell'] = ride['ar']['@pt']


            #$fahrt['ankunft']['zeitGeplant'] = $fahrt['ar']['@attributes']['pt'];
            #if(isset($sortAbweichung[$id]['ar']['@attributes']['ct'])){
            #$fahrt['ankunft']['zeitAktuell'] = $sortAbweichung[$id]['ar']['@attributes']['ct'];
            #}

            #$fahrt['ankunft']['gleisGeplant'] = $fahrt['ar']['@attributes']['pp'];
            #if(isset($sortAbweichung[$id]['ar']['@attributes']['cp'])){
            #$fahrt['ankunft']['gleisAktuell'] = $sortAbweichung[$id]['ar']['@attributes']['cp'];
            #}

            #$fahrt['ankunft']['routeGeplant'] = explode("|",$fahrt['ar']['@attributes']['ppth']);
            #if(isset($sortAbweichung[$id]['ar']['@attributes']['cpth'])){
            #$fahrt['ankunft']['routeAktuell'] = explode("|",$sortAbweichung[$id]['ar']['@attributes']['cpth']);
            #}

            #if(isset($sortAbweichung[$id]['ar']['@attributes']['cs'])){
            #$fahrt['ankunft']['cancel'] = $cancelstates[$sortAbweichung[$id]['ar']['@attributes']['cs']];
            #}
    return out


r = requests.get(apis['fahrplan-plus']['url']+'location/berlin', headers=headers)
print(r.status_code)
station = r.json()
print(station)
sid = station[2]['id']

print(apis['timetables']['url']+'fchg/'+str(sid))
r = requests.get(apis['timetables']['url']+'fchg/'+str(sid), headers=headers)
print(r.status_code)
abweichungen = xmltodict.parse(r.text)

url = apis['timetables']['url']+'plan/'+str(sid)+'/'+str(date)+'/'+str(hour)
print(url)
r = requests.get(url, headers=headers)
plan = xmltodict.parse(r.text)


for ride in abweichungen['timetable']['s']:
    if 'tl' in ride:
        id = ride['@id']
        owner = ride['tl']['@o']
        tclass = ride['tl']['@c']
        nr = ride['tl']['@n']
        print(id, owner, tclass, nr)
        print(parse_ar(ride))
        #break
