
# Extract the region between the brackets in the selected region name.
def extractRegionCode(region):
    regionCode = region[region.find("(")+1:region.find(")")]

    return regionCode

# Count the separating dashes of the region code.
def extractRegionType(subregion):
	if (len(subregion) == 3):
		subregion = subregion[0:2] #"US-" to "US".
		return "country"
	elif (subregion.count("-") == 2):
		return "subnational2"

	return "subnational1"
