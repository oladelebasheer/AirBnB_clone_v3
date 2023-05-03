#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get state_id (only one city)
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/states")
    r_j = r.json()
    
    state_id = None
    for state_j in r_j:
        rs = requests.get("http://0.0.0.0:5050/api/v1/states/{}/cities".format(state_j.get('id')))
        rs_j = rs.json()
        if len(rs_j) == 1: 
            state_id = state_j.get('id')
            break
    
    # Only Arizona
    
    """ POST /api/v1/places_search
    """
    r = requests.post("http://0.0.0.0:5050/api/v1/places_search", data=json.dumps({ 'states': [state_id] }), headers={ 'Content-Type': "application/json" })
    print(state_id)
    r_j = r.json()
    print(len(r_j))
