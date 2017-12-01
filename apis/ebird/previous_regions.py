"""
Return previous searches from repository.
"""
from persistence import redis_instance as connection

def save_previous_region(region):
    region_code = region[region.find("(")+1:region.find(")")]
    connection.save_key_value(region_code, region)

def get_previous_regions():
    return connection.get_values()

def clear_previous_regions():
    connection.clear_values()

def get_previous_regions_nonhash():
    return connection.get_values_nohash()
