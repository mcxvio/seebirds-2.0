""" Reformat functions. """
from datetime import datetime

def extract_date_time(value, dateortime):
    """ Extract date time. """
    obs_date_time = datetime.strptime(value, '%Y-%m-%d %H:%M')
    if dateortime == 'dt':
        return obs_date_time.strftime('%d-%b, %Y, %H:%M')
    elif dateortime == 'd':
        return obs_date_time.strftime('%d %B')
    elif dateortime == 'dx':
        return obs_date_time.strftime('%Y-%m-%d')

    return obs_date_time.strftime('%H:%M')

def extract_unique_date_times(response):
    """ Extract unique date time. """
    unique_dates = []
    for item in response:
        if not item['obsDt'] in unique_dates:
            unique_dates.append(item['obsDt'])
    return unique_dates

def extract_unique_dates(response):
    """ Extract unique dates. """
    unique_dates = []
    for item in response:
        if not extract_date_time(item['obsDt'], 'dx') in unique_dates:
            unique_dates.append(extract_date_time(item['obsDt'], 'dx'))
    return unique_dates

def remove_ob_items(observation):
    """ Remove observation items. """
    del observation['sciName']
    del observation['comName']
    #del ob['howMany']
    del observation['obsValid']
    del observation['obsReviewed']
    #return ob

def add_checklists_for_date(add_date, checklists, submission, submissions):
    """ Add checklists for date. """
    submission['obsDt'] = add_date
    submission['checklists'] = checklists
    submissions.append(submission)

def extract_region_code(region):
    """ Extract the region between the brackets in the selected region name. """
    if region.find("(") > 0: #Check for brackets.
        region_code = region[region.find("(")+1:region.find(")")]
        return region_code

    return region #Pass-through.

def extract_scientific_name(full_name):
    """ Extract scientific name. """
    if full_name.find("(") > 0: #Check for brackets.
        sci_name = full_name[full_name.find("(")+1:full_name.find(")")]
        return sci_name

    return full_name #Pass-through.

def extract_region_type(subregion):
    """ Count the separating dashes of the region code. """
    if len(subregion) == 3:
        subregion = subregion[0:2] #"US-" to "US".
        return "country"
    elif subregion.count("-") == 2:
        return "subnational2"

    return "subnational1"
