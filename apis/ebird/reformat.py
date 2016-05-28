from datetime import datetime

# Extract the region between the brackets in the selected region name.
def extractRegionCode(region):
    regionCode = region[region.find("(")+1:region.find(")")]

    return regionCode

def extractScientificName(fullName):
    sciName = fullName[fullName.find("(")+1:fullName.find(")")]

    return sciName

# Count the separating dashes of the region code.
def extractRegionType(subregion):
	if (len(subregion) == 3):
		subregion = subregion[0:2] #"US-" to "US".
		return "country"
	elif (subregion.count("-") == 2):
		return "subnational2"

	return "subnational1"

def extractDateTime(value, dateortime):
    obsDateTime = datetime.strptime(value, '%Y-%m-%d %H:%M')
    if dateortime == 'dt':
        return obsDateTime.strftime('%d-%b, %Y, %H:%M')
    elif dateortime == 'd':
        return obsDateTime.strftime('%d-%b')
    else:
        return obsDateTime.strftime('%H:%M')
