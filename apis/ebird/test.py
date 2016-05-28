from datetime import datetime
import requests
import json
from test_json import get_json

def extractDateTime(value, dateortime):
    obsDateTime = datetime.strptime(value, '%Y-%m-%d %H:%M')
    if dateortime == 'dt':
        return obsDateTime.strftime('%d-%b, %Y, %H:%M')
    elif dateortime == 'd':
        return obsDateTime.strftime('%d-%b')
    else:
        return obsDateTime.strftime('%H:%M')

#getjson = requests.get("http://ebird.org/ws1.1/data/obs/region/recent?rtype=subnational2&r=US-MA-025&hotspot=true&includeProvisional=true&back=5&fmt=json")
getjson = get_json()

response = json.loads(getjson)

uniqueDates = []
for item in response:
    if not item['obsDt'] in uniqueDates:
        uniqueDates.append(item['obsDt'])

#uniqueDates = set([x['obsDt'] for x in response if x['obsDt'] != None])
print("uniqueDates: ", uniqueDates)

#submission = {"obsDt": extractDateTime(item['obsDt'], 'd'), "checklists": [{"locID": item['locID'], "locName": item['locName'], "obsTm": extractDateTime(item['obsDt'], 't'), "speciesCount": speciesCount}]}

submissions = []
submission = {}
checklists = []
prevDate = "" #uniqueDates[0]
currDate = ""
chkCount = 0
for item in uniqueDates:
    currDate = extractDateTime(item, 'd')
    if prevDate == "":
        prevDate = currDate
    if prevDate != currDate:
        submission['obsDt'] = prevDate
        submission['checklists'] = checklists
        submissions.append(submission)
        submission = {}
        checklists = []
        prevDate = currDate

    obs = [x for x in response if x['obsDt'] == item]
    ob = obs[0]
    del ob['sciName']
    del ob['comName']
    del ob['howMany']
    del ob['obsValid']
    del ob['obsReviewed']
    ob['obsTm'] = extractDateTime(item, 't')
    ob['speciesCount'] = len(obs)
    checklists.append(ob)
    chkCount += 1
    print("......", ob)
    print("++++++", len(checklists))

submission['obsDt'] = currDate
submission['checklists'] = checklists
submissions.append(submission)
submissions.append({'chkCount': chkCount})
submission = {}
checklists = []

#print("___:::", submissions)
#print("___:::", len(submissions))
print("___:::", submissions)

'''

submissions = []
for item in response:
    dates = [x for x in response if x['obsDt'] == item['obsDt'] and x['locID'] == item['locID']]

    checklist = {"obsDt": extractDateTime(item['obsDt'], 'd'), "checklists": [{"locID": item['locID'], "locName": item['locName'], "obsTm": extractDateTime(item['obsDt'], 't'), "speciesCount": speciesCount}]}
    if not checklist in submissions:
        #speciesCount = [x for x in response if x['obsDt'] == item['obsDt']]
        #checklist['checklists'][0]['speciesCount'] = len(speciesCount)

        #print("checklist speciesCount: ", checklist['checklists'][0]['speciesCount'])
        #print("checklist speciesCount again: ", checklist['speciesCount'])

        speciesCount = len([x for x in response if x['obsDt'] == item['obsDt'] and x['locID'] == item['locID']])

        print("xxxxxxxxxx: ", item['obsDt'])
        print("yyyyyyyyyy: ", speciesCount)
        print("zzzzzzzzzz: ", checklist['checklists'][0]['speciesCount'])
        print("aaaaaaaaaa: ", checklist['checklists'][0]['locName'])
        print("-----------")

        submissions.append(checklist)

print("___:::", submissions)
'''