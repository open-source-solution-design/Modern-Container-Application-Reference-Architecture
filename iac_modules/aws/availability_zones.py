def availability_zones()
"""Use availability zones defined in the configuration file if available"""
    if config.get('az_list'):
        az_list = config.get_object('az_list')
    else:
        az_list = get_availability_zones(state="available").names
  
    return az_list

